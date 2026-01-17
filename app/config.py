"""Simple Configuration"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Ollama
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
    
    # Whisper
    WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")
    
    # App
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    
    # Directories
    UPLOAD_DIR = "/tmp/uploads"
    OUTPUT_DIR = "/tmp/outputs"


config = Config()
