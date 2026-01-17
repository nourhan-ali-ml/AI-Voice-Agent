"""Text-to-Speech with gTTS"""
import asyncio
from pathlib import Path
from loguru import logger
from gtts import gTTS
import uuid


class TTSService:
    def __init__(self):
        logger.info("✅ TTS initialized")
    
    async def synthesize(self, text: str, output_dir: Path) -> Path:
        """Convert text to speech"""
        logger.info(f"Synthesizing: {len(text)} chars")
        
        # Create output path
        output_dir.mkdir(parents=True, exist_ok=True)
        filename = f"tts_{uuid.uuid4()}.mp3"
        output_path = output_dir / filename
        
        # Generate speech
        def _generate():
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(str(output_path))
        
        await asyncio.to_thread(_generate)
        
        logger.success(f"✅ TTS saved: {filename}")
        return output_path


tts = TTSService()
