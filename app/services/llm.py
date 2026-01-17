"""LLM Service with Ollama"""
from loguru import logger
import ollama

from app.config import config


class OllamaAgent:
    def __init__(self):
        self.client = ollama.Client(host=config.OLLAMA_BASE_URL)
        self.model = config.OLLAMA_MODEL
        
        logger.info(f"Testing connection to Ollama at {config.OLLAMA_BASE_URL}")
        try:
            # Test connection
            self.client.list()
            logger.success(f"✅ Ollama connected: {self.model}")
        except Exception as e:
            logger.error(f"❌ Cannot connect to Ollama: {e}")
            logger.info("Make sure 'ollama serve' is running!")
    
    async def analyze_symptoms(self, patient_input: str) -> str:
        """Analyze patient symptoms and provide medical advice"""
        
        system_prompt = """You are a professional medical assistant. 
Analyze the patient's symptoms and provide:
1. Possible conditions (general, not diagnosis)
2. Recommended actions
3. When to seek immediate care

Be empathetic, clear, and always remind them to consult a healthcare professional."""
        
        logger.info(f"Analyzing: {patient_input[:50]}...")
        
        try:
            response = self.client.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": patient_input}
                ]
            )
            
            result = response['message']['content']
            logger.success(f"✅ Generated response: {len(result)} chars")
            return result
            
        except Exception as e:
            logger.error(f"❌ LLM error: {e}")
            return "I'm having trouble processing your request. Please ensure Ollama is running and try again."


llm = OllamaAgent()
