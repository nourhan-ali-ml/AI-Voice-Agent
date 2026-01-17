"""
Simple Medical Voice Agent
- Local Ollama LLM
- Local Whisper STT
- gTTS for TTS
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import sys

from app.config import config
from app.api.routes import router

# Configure logging
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
    level="INFO"
)

# Create app
app = FastAPI(
    title="Medical Voice Agent",
    description="AI-powered medical voice assistant using Ollama, Whisper, and gTTS",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router, prefix="/api")


@app.on_event("startup")
async def startup():
    logger.info("🚀 Starting Medical Voice Agent...")
    logger.info(f"📍 Ollama: {config.OLLAMA_BASE_URL}")
    logger.info(f"🤖 Model: {config.OLLAMA_MODEL}")
    logger.info(f"🎤 Whisper: {config.WHISPER_MODEL}")
    logger.success("✅ Application started successfully!")


@app.on_event("shutdown")
async def shutdown():
    logger.info("👋 Shutting down...")


@app.get("/")
async def root():
    return {
        "message": "Medical Voice Agent API",
        "docs": "/docs",
        "health": "/api/health",
        "endpoints": {
            "voice_call": "POST /api/voice-call (upload audio)",
            "text_query": "POST /api/text-query (send JSON)",
            "download": "GET /api/download/{filename}"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=config.PORT)
