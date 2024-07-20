import os
import time
import uuid
import json
from pathlib import Path
from datetime import datetime
import threading

from flask import Flask, render_template, request, send_from_directory, jsonify
import requests

from openai import OpenAI

from elevenlabs import Voice, VoiceSettings, play
from elevenlabs.client import ElevenLabs


app = Flask(__name__)
client = OpenAI()

API_KEY = os.environ.get('OPENAI_API_KEY')
XI_API_KEY = os.environ.get('ELEVENLABS_API_KEY')
my_assistant_id = 'asst_vTvJBSCPMwz4aDVjoOGu40pD'
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
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_file, "a") as f:
            f.write(f"[{timestamp}] {user_input}\n")
            f.write('\n')

        # Let's create a thread variable that's gonna call the OpenAI APIs
        thread = client.beta.threads.create()

        # Let's create a message object to send to Assistant API
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_input
        )

        # Let's call the run command on the Assistant API
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=my_assistant_id
        )

        # This loops the request status and logs when reply comes back from OpenAI
        check_status(thread.id)

        # This retrieves message from thread and extracts response 
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        response_text = messages.data[0].content[0].text.value

        # Generate the audio file from response_text
        speech_file_path = Path(__file__).parent / "static/response.mp3"
        audio_file = 'static/response.mp3'

        # Call to OpenAI TTS API
        response = client.audio.speech.create(
            model="tts-1",
            voice="onyx",
            input=response_text
        )
        response.stream_to_file(speech_file_path)

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

def check_status(thread_id):
    count = 0
    while True:
        runs = client.beta.threads.runs.list(thread_id=thread_id)
        status = runs.data[0].status
        print(count, status)

        if status == 'completed':
            break
        elif status == 'failed':
            print(runs)
            raise Exception("Run failed")
        else:
            time.sleep(1)
            count += 1

if __name__ == '__main__':
    app.run(debug=True)