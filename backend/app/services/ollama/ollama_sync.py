"""
Synchronous Ollama service for backwards compatibility.
This version uses requests instead of aiohttp for simpler deployment.
"""
import time
import requests
import logging
from typing import Dict, Any, Optional

from app.core.config import settings
from app.services.base import LLMService


class OllamaService(LLMService):
    """Service for interacting with Ollama API using synchronous requests."""
    
    def __init__(self, model: str, base_url: Optional[str] = None):
        super().__init__()
        self.model = model
        self.base_url = base_url or settings.ollama_url
        self.timeout = 60  # seconds
    
    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate response from Ollama (async wrapper for sync call)."""
        self.logger.info(f"Generating response with model: {self.model}")
        self.logger.debug(f"Prompt: {prompt[:100]}...")
        
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                **kwargs
            }
            
            start_time = time.time()
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code != 200:
                raise Exception(f"Ollama API error {response.status_code}: {response.text}")
            
            data = response.json()
            end_time = time.time()
            
            self.logger.info(f"Response generated in {end_time - start_time:.2f}s")
            return data.get("response", "").strip()
                
        except Exception as e:
            self.logger.error(f"Error generating response: {e}")
            raise
    
    async def is_available(self) -> bool:
        """Check if Ollama service is available."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            return response.status_code == 200
        except Exception as e:
            self.logger.error(f"Ollama service unavailable: {e}")
            return False
    
    async def close(self):
        """No-op for requests-based implementation."""
        pass
