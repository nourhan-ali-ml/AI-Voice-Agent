"""API Routes"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
import shutil
import uuid
from loguru import logger

from app.config import config
from app.services.stt import stt
from app.services.llm import llm
from app.services.tts import tts

router = APIRouter()

# Create directories
UPLOAD_DIR = Path(config.UPLOAD_DIR)
OUTPUT_DIR = Path(config.OUTPUT_DIR)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Medical Voice Agent",
        "ollama_url": config.OLLAMA_BASE_URL,
        "ollama_model": config.OLLAMA_MODEL,
        "whisper_model": config.WHISPER_MODEL
    }


@router.post("/voice-call")
async def process_voice_call(audio: UploadFile = File(...)):
    """
    Process a voice call:
    1. Convert speech to text (STT)
    2. Analyze with LLM
    3. Convert response to speech (TTS)
    4. Return audio file
    """
    try:
        logger.info(f"📞 New voice call: {audio.filename}")
        
        # Save uploaded audio
        audio_id = str(uuid.uuid4())
        input_path = UPLOAD_DIR / f"{audio_id}_{audio.filename}"
        
        with open(input_path, "wb") as f:
            shutil.copyfileobj(audio.file, f)
        
        logger.info(f"📥 Saved audio: {input_path.name}")
        
        # Step 1: Speech to Text
        logger.info("🎤 Step 1: Transcribing audio...")
        transcribed_text = await stt.transcribe(input_path)
        logger.info(f"📝 Patient said: {transcribed_text}")
        
        # Step 2: LLM Analysis
        logger.info("🤖 Step 2: Analyzing with LLM...")
        llm_response = await llm.analyze_symptoms(transcribed_text)
        logger.info(f"💬 AI response: {llm_response[:100]}...")
        
        # Step 3: Text to Speech
        logger.info("🔊 Step 3: Converting to speech...")
        output_audio_path = await tts.synthesize(llm_response, OUTPUT_DIR)
        
        # Cleanup input file
        input_path.unlink()
        
        logger.success(f"✅ Voice call completed: {output_audio_path.name}")
        
        # Return results
        return {
            "success": True,
            "patient_input": transcribed_text,
            "ai_response": llm_response,
            "audio_file": f"/download/{output_audio_path.name}",
            "message": "Voice call processed successfully"
        }
        
    except Exception as e:
        logger.error(f"❌ Error processing voice call: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download/{filename}")
async def download_audio(filename: str):
    """Download generated audio file"""
    file_path = OUTPUT_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        media_type="audio/mpeg",
        filename=filename
    )


@router.post("/text-query")
async def text_query(query: dict):
    """
    Text-only endpoint (no voice)
    Send: {"text": "I have a headache"}
    """
    try:
        text = query.get("text", "")
        if not text:
            raise HTTPException(status_code=400, detail="Text is required")
        
        logger.info(f"📝 Text query: {text}")
        
        # Analyze with LLM
        response = await llm.analyze_symptoms(text)
        
        return {
            "success": True,
            "input": text,
            "response": response
        }
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
