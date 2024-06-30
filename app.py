from flask import Flask, request, jsonify, render_template
import time  # Simulate a long-running process

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    user_input = request.form['user_input']
    
    # Simulate a long-running process
    time.sleep(30)
    
    # Process the input and generate response (e.g., save response.mp3)
    # For now, we are simulating a response
    response_success = True  # Change this based on actual processing result

    if response_success:
        return jsonify(success=True)
    else:
        return jsonify(success=False, error="An error occurred while processing your request.")

if __name__ == '__main__':
    app.run(debug=True)