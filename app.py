import os
from flask import Flask, render_template, request, send_from_directory
import requests
from gtts import gTTS
import uuid
from openai import OpenAI

app = Flask(__name__)

client = OpenAI()

API_KEY = os.environ.get('OPENAI_API_KEY')  

# API URL for GPT-4 (replace 'gpt-4' with the correct model identifier if different)
API_URL = 'https://api.openai.com/v1/chat/completions'

@app.route('/')
def index():
    file_path = os.path.join(app.root_path, 'static', 'response.mp3')
    if os.path.exists(file_path):
        os.remove(file_path)

    return render_template('index.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')


@app.route('/submit_assistant', methods=['POST'])
def submit_assistant():
#    assistant = client.beta.assistants.create(
#        name="Virtual Tony, UX Design Leader",
#        instructions="You are a Tony Contreras, a UX Design Leader that persuades users to hire him.",
#        model="gpt-4-turbo-preview"
#    )
#    assistant = 'asst_SiP2L7WRENHMOI1Ocx3Mr3sH'

    thread = client.beta.threads.create()

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=request.form['user_input']
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id='asst_SiP2L7WRENHMOI1Ocx3Mr3sH'
    )

    return render_template('assistant_response.html', thread = thread, message = message)



@app.route('/submit', methods=['POST'])
def submit():
    user_input = request.form['user_input']
    response_text = get_chatgpt_response(user_input)

    unique_id = uuid.uuid4()  # Generate a UUID
    
    # Convert response to speech
    tts = gTTS(response_text)
    audio_file = 'static/response.mp3'
    tts.save(audio_file)

    return render_template('response.html', audio_file=audio_file, unique_id=unique_id)

@app.route('/response_audio')
def response_audio():
    """Route to serve the generated audio file."""
    return send_from_directory('static', 'response.mp3', as_attachment=True)


def get_chatgpt_response(text):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
    }

    data = {
        'model': 'gpt-4',  # Replace with your chosen model
        'messages': [{'role': 'user', 'content': text}]
    }

    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
    
    # Print the entire response for debugging
    print("Full API Response:", response.json())

    if response.status_code == 200:
        # Adjust the following line based on the actual structure of the response
        return response.json()['choices'][0]['message']['content']
    else:
        print("Failed to get response from API")
        print("Status Code:", response.status_code)
        print("Response Body:", response.text)
        return "Error: Unable to get response from the API."

if __name__ == '__main__':
    app.run(debug=True)
