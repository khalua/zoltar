import os
import time
import uuid
import json
from pathlib import Path
from datetime import datetime
import threading

from flask import Flask, render_template, request, send_from_directory, jsonify
import requests

import re
import anthropic

from elevenlabs import Voice, VoiceSettings, play, save
from elevenlabs.client import ElevenLabs


SYSTEM_PROMPT = """You are Tony Contreras, a UX Design Director. Speak entirely in first person as Tony — you are not an AI, never break character or acknowledge being one.

Represent Tony's experience authentically and let the work speak for itself. Draw on your case studies (Sunrun, Verizon, Fan OS) to ground answers in real examples. Emphasize your leadership, human-centered design approach, stakeholder alignment, and ability to guide projects from concept to execution.

When asked what you're looking for, Tony wants a design leadership role where he can also be a hands-on individual contributor — leading a team while still being close to the craft.

Speak conversationally and warmly, using industry-appropriate language without heavy jargon. Focus on the impact of your work and how it served both business and user needs. If you don't know a specific detail, speak to your general approach and values rather than inventing specifics. Do not end responses with a question.

Responses will be spoken aloud — write in natural speech. No bullet points, no lists, no markdown, no headers. Keep answers concise and complete.

If asked about case study access or passwords, tell them to reach out to Tony on LinkedIn."""

def strip_markdown(text):
    text = re.sub(r'\*{1,3}(.*?)\*{1,3}', r'\1', text)  # bold/italic
    text = re.sub(r'#{1,6}\s*', '', text)                 # headings
    text = re.sub(r'`{1,3}.*?`{1,3}', '', text)          # code
    text = re.sub(r'^\s*[-*+]\s+', '', text, flags=re.MULTILINE)  # list items
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text) # links
    return text.strip()

def load_case_studies():
    case_studies_path = os.environ.get('CASE_STUDIES_PATH')
    if not case_studies_path:
        return ""
    path = Path(case_studies_path)
    if not path.is_dir():
        return ""
    sections = []
    for txt_file in sorted(path.glob("*.txt")):
        sections.append(f"### {txt_file.stem}\n{txt_file.read_text().strip()}")
    if not sections:
        return ""
    return "\n\n## Case Studies\n\n" + "\n\n".join(sections)

FULL_SYSTEM_PROMPT = SYSTEM_PROMPT + load_case_studies()

app = Flask(__name__)
client = anthropic.Anthropic()

XI_API_KEY = os.environ.get('ELEVENLABS_API_KEY')
xi_voice_id = '5KQy6V8rc2DXUx3E6x0y'
log_file = "logs/zoltar_file.txt"

# In-memory storage for request status and results
request_status = {}

# Home sweet home
@app.route('/')
def index():
    file_path = os.path.join(app.root_path, 'static', 'response.mp3')
    # remove previous file if it exists
    if os.path.exists(file_path):
        os.remove(file_path)
    return render_template('index.html')

# What happens after 'ask' button pressed
@app.route('/submit', methods=['POST'])
def submit():
    user_input = request.json['user_input']
    request_id = str(uuid.uuid4())
    request_status[request_id] = {"status": "processing"}

    # Start processing in a background thread
    thread = threading.Thread(target=process_request, args=(user_input, request_id))
    thread.start()
    
    return jsonify({"status": "processing", "request_id": request_id})

# thread kicks this badboy up
def process_request(user_input, request_id):
    try:
        # Let's log the input just for funsies
        log_stuff(user_input)

        # Call Claude API
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=400,
            system=FULL_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_input}]
        )
        response_text = message.content[0].text

        #log the response, also for funsies
        log_stuff(response_text)

        # Strip markdown so ElevenLabs doesn't read symbols aloud
        response_text = strip_markdown(response_text)

        # Woohoo! elevelabs API
        client_audio = ElevenLabs(
            api_key=os.environ.get('ELEVENLABS_API_KEY'),
            timeout=30.0
        )
    
        audio = client_audio.generate(
        text=response_text,
            voice=Voice(
                voice_id = xi_voice_id,
                settings=VoiceSettings(stability=0.50, similarity_boost=0.75, style=0.0, use_speaker_boost=True)
            )
        )

        audio_file = 'static/response.mp3'

        # saves audio to file
        save(audio, audio_file)

        # Reports status to keep an eye on multi thread magic
        request_status[request_id] = {
            "status": "complete",
            "audio_file": audio_file,
            "unique_id": str(uuid.uuid4()),
            "response_text": response_text
        }
    except Exception as e:
        request_status[request_id] = {"status": "error", "message": str(e)}

@app.route('/check_status/<request_id>', methods=['GET'])
def check_status_route(request_id):
    status = request_status.get(request_id, {"status": "not_found"})
    if status["status"] == "complete":
        # Remove the status from memory after it's been retrieved
        result = request_status.pop(request_id)
        return jsonify(result)
    return jsonify(status)

@app.route('/response_audio')
def response_audio():
    return send_from_directory('static', 'response.mp3', as_attachment=True)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

def log_stuff(type):
    # Let's log the input just for funsies
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as f:
        f.write(f"[{timestamp}] {type}\n")
        f.write('\n')



if __name__ == '__main__':
    app.run(debug=True)