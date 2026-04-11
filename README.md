# ChatGPTony - AI-Powered Interactive Resume

An interactive web application that brings Tony's professional experience to life through AI conversation and voice synthesis. Perfect for recruiters, hiring managers, and anyone curious about Tony's background!

## What This Application Does

ChatGPTony is a fun way to learn about Tony's professional's background. Instead of reading a static resume, you can have a natural conversation with an AI that knows all about Tony's experience, skills, and personality. The AI responds both in text and with realistic voice audio, complete with ridiculous animated facial expressions.

### Key Features

* **Interactive Q&A**: Ask questions about Tony's experience, skills, or career goals
* **Voice Responses**: Hear answers spoken aloud using realistic AI-generated voice
* **Visual Animation**: Watch Tony's face animate while speaking
* **Pre-loaded Questions**: Quick-start prompts for common interview questions
* **Real-time Processing**: Seamless conversation flow with live status updates

## How It Works (Technical Overview)

### Anthropic Claude Integration

The application uses Anthropic's Claude API to create an intelligent conversational agent:

* **Custom System Prompt**: Detailed persona and background context injected on every request
* **Case Study Context**: Private case study files loaded at server startup and included in each request
* **Smart Responses**: Leverages Claude Haiku for fast, high-quality conversational responses

### ElevenLabs Voice Synthesis

For realistic voice responses:

* **Text-to-Speech**: Converts AI responses into natural-sounding audio
* **Voice Cloning**: Uses a custom voice profile that sounds like Tony
* **Real-time Generation**: Creates audio files on-demand for each response

### Interactive Frontend

* **Responsive Design**: Works on desktop and mobile devices
* **Animation System**: JavaScript-powered facial animation synchronized with audio
* **Polling System**: Efficiently checks response status without blocking the interface
* **Cached Responses**: Pre-generated audio for common questions for faster loading

### Cloud Deployment

The application is deployed on a DigitalOcean virtual server using modern containerization technology:

* **DigitalOcean Droplet**: Cloud-based virtual private server for reliable hosting
* **Docker Containers**: Application runs in isolated, reproducible containers
* **Dokku Platform**: Heroku-like deployment platform for easy management
* **Automatic HTTPS**: SSL certificates via Let's Encrypt for secure connections
* **Nginx Reverse Proxy**: Efficient request routing and load balancing
* **Environment Variables**: Secure API key management through configuration

## Architecture Flow

1. **User Interaction**: Visitor types a question or clicks a suggested prompt
2. **Backend Processing**: Flask server receives the question and starts background processing
3. **AI Processing**: Anthropic Claude API generates an intelligent response
4. **Voice Generation**: ElevenLabs converts the text response to natural speech
5. **Response Delivery**: Audio file and text are sent back to the user's browser
6. **Visual Feedback**: Face animation plays synchronized with the audio

## Technical Stack

* **Backend**: Python Flask web framework
* **AI Engine**: Anthropic Claude API (Haiku)
* **Voice Synthesis**: ElevenLabs API
* **Frontend**: HTML5, CSS3, JavaScript (with GSAP animation)
* **Deployment Platform**: Dokku (open-source PaaS)
* **Infrastructure**: DigitalOcean Droplet (Ubuntu 24.04)
* **Containerization**: Docker
* **Web Server**: Nginx with SSL/TLS
* **Audio Processing**: Real-time MP3 generation and streaming

## For Recruiters & Hiring Managers

This project demonstrates several valuable technical and creative skills:

### **Technical Competencies**

* **API Integration**: Successfully integrates multiple third-party services
* **Asynchronous Processing**: Handles long-running AI requests without blocking users
* **Performance Optimization**: Implements caching and efficient polling mechanisms
* **Cloud Infrastructure**: Production deployment on scalable cloud infrastructure
* **DevOps Knowledge**: Container management, reverse proxies, and SSL configuration
* **Full-Stack Development**: Complete end-to-end application development

### **Problem-Solving Skills**

* **User Experience**: Creates engaging, interactive experience for resume viewing
* **Performance Engineering**: Optimizes response times and resource usage
* **Error Handling**: Robust timeout and retry mechanisms
* **Scalability**: Architecture supports multiple concurrent users
* **Infrastructure Design**: Efficient use of cloud resources and containerization

### **Innovation & Creativity**

* **Novel Approach**: Transforms traditional resume into interactive experience
* **Technology Integration**: Combines AI, voice synthesis, and web technologies
* **User-Centric Design**: Focuses on making information accessible and engaging

## Deployment Architecture

The application uses a modern, production-ready deployment stack:

### Docker Containerization
The application runs in Docker containers, providing:
- **Isolation**: Consistent runtime environment regardless of host system
- **Reproducibility**: Identical behavior across development and production
- **Resource Efficiency**: Lightweight virtualization with minimal overhead
- **Easy Updates**: Simple container replacement for application updates

### Dokku Platform
Dokku provides a Heroku-like experience on your own server:
- **Git-Based Deployment**: Push code changes via Git to automatically deploy
- **Buildpack Detection**: Automatically detects and configures Python applications
- **Environment Management**: Secure configuration through environment variables
- **Zero-Downtime Deploys**: Health checks ensure smooth updates
- **SSL Management**: Automatic HTTPS certificate provisioning and renewal

### Infrastructure Components
- **DigitalOcean Droplet**: Ubuntu-based virtual server with dedicated resources
- **Nginx**: High-performance reverse proxy handling SSL termination and routing
- **Let's Encrypt**: Free, automated SSL/TLS certificates
- **DNS Configuration**: Wildcard DNS enables multiple app deployments

## Getting Started (For Developers)

### Prerequisites

* Python 3.8+
* Anthropic API key
* ElevenLabs API key

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
export ANTHROPIC_API_KEY="your-anthropic-key"
export ELEVENLABS_API_KEY="your-elevenlabs-key"

# Run the application
python3 app.py
```

### Deployment to Dokku

The application is configured for simple Git-based deployment:

```bash
# Add Dokku remote (one-time setup)
git remote add dokku dokku@your-server-ip:zoltar

# Deploy application
git push dokku main

# Set environment variables on server
ssh root@your-server-ip
dokku config:set zoltar ANTHROPIC_API_KEY="your-key"
dokku config:set zoltar ELEVENLABS_API_KEY="your-key"
dokku config:set zoltar CASE_STUDIES_PATH=/home/dokku/zoltar/case-studies

# Enable HTTPS
dokku letsencrypt:enable zoltar
```

The deployment process:
1. Detects Python application via requirements.txt
2. Installs dependencies in isolated container
3. Starts application using Procfile configuration
4. Configures Nginx reverse proxy
5. Provisions SSL certificate
6. Routes traffic to your domain

## Try It Out!

Visit the live application and ask questions like:
- "Should I hire you?"
- "Tell me about your notable accomplishments"
- "What kind of company do you want to work for?"
- "What's your experience with [specific technology]?"

---

*This project showcases the intersection of AI technology, web development, and creative user experience design.*