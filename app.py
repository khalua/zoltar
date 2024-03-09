import os
import time
import uuid
import json
from pathlib import Path
from datetime import datetime

from flask import Flask, render_template, request, send_from_directory
import requests

from openai import OpenAI  

app = Flask(__name__)

client = OpenAI()

API_KEY = os.environ.get('OPENAI_API_KEY')  

log_file = "logs/zoltar_file.txt"

# API & Assistant ID URL for GPT-4 (replace 'gpt-4' with the correct model identifier if different)
API_URL = 'https://api.openai.com/v1/chat/completions'
my_assistant_id = 'asst_vTvJBSCPMwz4aDVjoOGu40pD'

@app.route('/')
def index():
    file_path = os.path.join(app.root_path, 'static', 'response.mp3')
    if os.path.exists(file_path):
        os.remove(file_path)

    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    user_input = request.form['user_input']
    print(user_input) #print user input for debugging

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Get current timestamp

    # Append the JSON response to a file
    with open(log_file, "a") as f:
        f.write(timestamp + '\n')  # Add timestamp
        f.write(user_input + '\n') # Log request
        f.write('\n')  # Add a newline to separate each appended response

    ## create the thread to ask a question
    thread = client.beta.threads.create()
    # print (thread)

    ## package up the message from the user
    message = client.beta.threads.messages.create(
        thread_id = thread.id,
        role = "user",
        content=user_input
    )
    # print(message)

    ##create a run to associate the assistant to this request
    run = client.beta.threads.runs.create(
        thread_id = thread.id,
        assistant_id = 'asst_vTvJBSCPMwz4aDVjoOGu40pD'
    )
    # print(run)

    # check status
    while True:
        runs = client.beta.threads.runs.list(
        thread_id = thread.id
        )
        status = runs.data[0].status

        #check if it's completed
        if status == 'completed':
            break;
        else:
            time.sleep(1)

    # the messy message object
    messages = client.beta.threads.messages.list(
    thread_id=thread.id
    )

    # the cleaned up response
    response_text = messages.data[0].content[0].text.value

    unique_id = uuid.uuid4()  # Generate a UUID
    
    #now using Open AI text to speech!
    speech_file_path = Path(__file__).parent / "static/response.mp3"
    audio_file = 'static/response.mp3'
    response = client.audio.speech.create(
        model="tts-1",
        voice="onyx",
        input=response_text
    )
    response.stream_to_file(speech_file_path)

    return render_template('index.html', audio_file=audio_file, unique_id=unique_id)


@app.route('/response_audio')
def response_audio():
    """Route to serve the generated audio file."""
    return send_from_directory('static', 'response.mp3', as_attachment=True)

## helper functions ##
#check status function baby!
def check_status(thread_id):
    while True:
        runs = client.beta.threads.runs.list(
        thread_id = thread.id
        )
        status = runs.data[0].status

        #check if it's completed
        if status == 'completed':
            break;
        else:
            time.sleep(1)

def get_chatgpt_response(text):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
    }

    data = {
        'model': 'gpt-3.5-turbo',  # Replace with your chosen model
        'messages': [{'role': 'user', 'content': text}]
    }

    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
    
    # Print the entire response for debugging
    print("Full API Response:", response.json())

    # Get current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Append the JSON response to a file
    with open(log_file, "a") as f:
        f.write(timestamp + '\n')  # Add timestamp
        json.dump(response.json(), f, indent=4)
        f.write('\n')  # Add a newline to separate each appended response

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