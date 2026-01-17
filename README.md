# 🏥 Medical Voice Agent

**100% Free & Mostly Local** - AI-powered medical voice assistant

## ✨ Features

- 🎤 **Speech-to-Text**: Whisper (local)
- 🤖 **AI Analysis**: Ollama (llama3.2:3b)
- 🔊 **Text-to-Speech**: gTTS
- 🌐 **Simple API**: 3 endpoints only
- 🚀 **Fast Setup**: 5 minutes

## 📋 Prerequisites

1. **Ollama** - Download from https://ollama.com/download
2. **Docker Desktop** - For Windows/Mac
3. **8GB RAM minimum**

## 🚀 Quick Start

### Step 1: Install Ollama

```bash
# Download and install Ollama
# Then download the model:
ollama pull llama3.2:3b
```

### Step 2: Start Ollama

```bash
# Keep this running in a separate terminal:
ollama serve
```

### Step 3: Build & Run

```bash
# Extract the project
cd simple-voice-agent

# Build and start
docker-compose up -d

# View logs
docker-compose logs -f app
```

### Step 4: Wait for Whisper to Load

First startup takes **2-3 minutes** to download Whisper model.

You'll see:
```
✅ Whisper loaded
✅ Ollama connected
✅ Application started successfully!
```

### Step 5: Test!

Open browser: **http://localhost:8000/docs**

## 📡 API Endpoints

### 1. Health Check
```bash
GET http://localhost:8000/api/health
```

### 2. Voice Call (Main Feature)
```bash
POST http://localhost:8000/api/voice-call
Content-Type: multipart/form-data

# Upload audio file
audio: your_audio.mp3
```

**Response:**
```json
{
  "success": true,
  "patient_input": "I have a headache and fever",
  "ai_response": "Based on your symptoms...",
  "audio_file": "/download/tts_xxx.mp3"
}
```

### 3. Text Query (No Voice)
```bash
POST http://localhost:8000/api/text-query
Content-Type: application/json

{
  "text": "I have a headache"
}
```

### 4. Download Audio
```bash
GET http://localhost:8000/download/{filename}
```

## 🧪 Testing with Swagger UI

1. Open: http://localhost:8000/docs
2. Click on **POST /api/voice-call**
3. Click **Try it out**
4. Upload an audio file (mp3, wav, m4a)
5. Click **Execute**
6. Download the response audio!

## 🛠️ Configuration

Edit `.env` file:

```env
# Ollama
OLLAMA_BASE_URL=http://host.docker.internal:11434
OLLAMA_MODEL=llama3.2:3b

# Whisper (tiny, base, small, medium, large)
WHISPER_MODEL=base

# Server
PORT=8000
DEBUG=false
```

## 📊 System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| RAM | 8 GB | 16 GB |
| Storage | 5 GB | 10 GB |
| CPU | 4 cores | 8 cores |

## 🔧 Troubleshooting

### "Cannot connect to Ollama"
```bash
# Make sure Ollama is running:
ollama serve

# Check if model is downloaded:
ollama list
```

### "Application startup slow"
First startup downloads Whisper model (~150MB). Wait 2-3 minutes.

### "Out of memory"
Use smaller Whisper model in `.env`:
```env
WHISPER_MODEL=tiny
```

## 📁 Project Structure

```
simple-voice-agent/
├── app/
│   ├── main.py           # FastAPI app
│   ├── config.py         # Configuration
│   ├── api/
│   │   └── routes.py     # API endpoints
│   └── services/
│       ├── stt.py        # Speech-to-Text
│       ├── tts.py        # Text-to-Speech
│       └── llm.py        # Ollama LLM
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env
```

## 🎯 Example Usage

### Using cURL:

```bash
# Text query
curl -X POST http://localhost:8000/api/text-query \
  -H "Content-Type: application/json" \
  -d '{"text": "I have a headache and feel dizzy"}'

# Voice call
curl -X POST http://localhost:8000/api/voice-call \
  -F "audio=@recording.mp3"
```

### Using Python:

```python
import requests

# Text query
response = requests.post(
    "http://localhost:8000/api/text-query",
    json={"text": "I have a fever"}
)
print(response.json())

# Voice call
with open("audio.mp3", "rb") as f:
    response = requests.post(
        "http://localhost:8000/api/voice-call",
        files={"audio": f}
    )
    result = response.json()
    print(result["ai_response"])
```

## 🔄 Commands

```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# View logs
docker-compose logs -f app

# Rebuild
docker-compose build --no-cache

# Restart
docker-compose restart app
```

## 💰 Cost

**100% FREE!**
- ✅ Ollama: Free
- ✅ Whisper: Free
- ✅ gTTS: Free (requires internet for TTS only)

## ⚠️ Disclaimer

This project is intended for educational and demonstration purposes only.
It is not a medical device and does not provide professional medical advice.
Always consult qualified healthcare professionals.

## 📝 License

MIT License - Use freely!

## 🤝 Support

Having issues? Check:
1. Ollama is running: `ollama serve`
2. Model is downloaded: `ollama list`
3. Docker is running
4. Logs: `docker-compose logs -f app`

---

## 🎓 Why this project?
This project was built to demonstrate how to design a complete AI voice pipeline
(STT → LLM → TTS) using open-source tools, Docker, and clean API design.
