# ChatGPTony - AI-Powered Interactive Resume 

An interactive web application that brings Tony's professional experience to life through AI conversation and voice synthesis. Perfect for recruiters, hiring managers, and anyone curious about Tony's background!

## What This Application Does

ChatGPTony is a fun way to learn about Tony's professional's background. Instead of reading a static resume, you can have a natural conversation with an AI that knows all about Tony's experience, skills, and personality. The AI responds both in text and with realistic voice audio, complete with ridiculous animated facial expressions.

### Key Features
- **Interactive Q&A**: Ask questions about Tony's experience, skills, or career goals
- **Voice Responses**: Hear answers spoken aloud using realistic AI-generated voice
- **Visual Animation**: Watch Tony's face animate while speaking
- **Pre-loaded Questions**: Quick-start prompts for common interview questions
- **Real-time Processing**: Seamless conversation flow with live status updates

## How It Works (Technical Overview)

### 🤖 OpenAI Integration
The application uses OpenAI's Assistant API to create an intelligent conversational agent:
- **Custom Assistant**: Pre-trained with Tony's professional background, experiences, and personality
- **Thread Management**: Each conversation creates a unique thread for context retention
- **Smart Responses**: Leverages GPT's natural language understanding for human-like interactions

### 🗣️ ElevenLabs Voice Synthesis
For realistic voice responses:
- **Text-to-Speech**: Converts AI responses into natural-sounding audio
- **Voice Cloning**: Uses a custom voice profile that sounds like Tony
- **Real-time Generation**: Creates audio files on-demand for each response

### 🎨 Interactive Frontend
- **Responsive Design**: Works on desktop and mobile devices
- **Animation System**: JavaScript-powered facial animation synchronized with audio
- **Polling System**: Efficiently checks response status without blocking the interface
- **Cached Responses**: Pre-generated audio for common questions for faster loading

### ☁️ Heroku Deployment
The application is deployed on Heroku's cloud platform:
- **Scalable Hosting**: Automatically handles traffic spikes
- **Environment Variables**: Secure API key management
- **Continuous Deployment**: Updates automatically when code changes
- **Procfile Configuration**: Optimized for production with Gunicorn server

## Architecture Flow

1. **User Interaction**: Visitor types a question or clicks a suggested prompt
2. **Backend Processing**: Flask server receives the question and starts background processing
3. **AI Processing**: OpenAI Assistant API generates an intelligent response
4. **Voice Generation**: ElevenLabs converts the text response to natural speech
5. **Response Delivery**: Audio file and text are sent back to the user's browser
6. **Visual Feedback**: Face animation plays synchronized with the audio

## Technical Stack

- **Backend**: Python Flask web framework
- **AI Engine**: OpenAI Assistant API (GPT-4 based)
- **Voice Synthesis**: ElevenLabs API
- **Frontend**: HTML5, CSS3, JavaScript (with GSAP animation)
- **Deployment**: Heroku cloud platform
- **Audio Processing**: Real-time MP3 generation and streaming

## For Recruiters & Hiring Managers

This project demonstrates several valuable technical and creative skills:

### **Technical Competencies**
- **API Integration**: Successfully integrates multiple third-party services
- **Asynchronous Processing**: Handles long-running AI requests without blocking users
- **Performance Optimization**: Implements caching and efficient polling mechanisms
- **Cloud Deployment**: Production-ready deployment on Heroku
- **Full-Stack Development**: Complete end-to-end application development

### **Problem-Solving Skills**
- **User Experience**: Creates engaging, interactive experience for resume viewing
- **Performance Engineering**: Optimizes response times and resource usage
- **Error Handling**: Robust timeout and retry mechanisms
- **Scalability**: Architecture supports multiple concurrent users

### **Innovation & Creativity**
- **Novel Approach**: Transforms traditional resume into interactive experience
- **Technology Integration**: Combines AI, voice synthesis, and web technologies
- **User-Centric Design**: Focuses on making information accessible and engaging

## Getting Started (For Developers)

### Prerequisites
- Python 3.8+
- OpenAI API key
- ElevenLabs API key

### Local Development
```bash
# Clone the repository
git clone [repository-url]
cd zoltar

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY="your-openai-key"
export ELEVENLABS_API_KEY="your-elevenlabs-key"

# Run the application
python3 app.py

### Deployment
The application is configured for Heroku deployment

## Try It Out!

Visit the live application and ask questions like:
- "Should I hire you?"
- "Tell me about your notable accomplishments"
- "What kind of company do you want to work for?"
- "What's your experience with [specific technology]?"

---

*This project showcases the intersection of AI technology, web development, and creative user experience design.*