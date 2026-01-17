"""Speech-to-Text with Whisper"""
import asyncio
from pathlib import Path
from loguru import logger
import whisper

from app.config import config


class WhisperSTT:
    def __init__(self):
        logger.info(f"Loading Whisper model: {config.WHISPER_MODEL}")
        self.model = whisper.load_model(config.WHISPER_MODEL)
        logger.success(f"✅ Whisper loaded")
    
    async def transcribe(self, audio_path: Path) -> str:
        """Transcribe audio to text"""
        logger.info(f"Transcribing: {audio_path.name}")
        
        result = await asyncio.to_thread(
            self.model.transcribe,
            str(audio_path),
            fp16=False
        )
        
        text = result["text"].strip()
        logger.success(f"✅ Transcribed: {len(text)} chars")
        return text


stt = WhisperSTT()
