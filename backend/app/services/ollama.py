"""
Ollama service for LLM interactions.
"""
import asyncio
import time
from typing import Dict, Any, Optional
import aiohttp
import logging

from app.core.config import settings
from app.services.base import LLMService


class OllamaService(LLMService):
    """Service for interacting with Ollama API."""
    
    def __init__(self, model: str, base_url: Optional[str] = None):
        super().__init__()
        self.model = model
        self.base_url = base_url or settings.ollama_url
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session."""
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=60)
            self.session = aiohttp.ClientSession(timeout=timeout)
        return self.session
    
    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate response from Ollama."""
        self.logger.info(f"Generating response with model: {self.model}")
        self.logger.debug(f"Prompt: {prompt[:100]}...")
        
        try:
            session = await self._get_session()
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                **kwargs
            }
            
            start_time = time.time()
            async with session.post(
                f"{self.base_url}/api/generate",
                json=payload
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Ollama API error {response.status}: {error_text}")
                
                data = await response.json()
                end_time = time.time()
                
                self.logger.info(f"Response generated in {end_time - start_time:.2f}s")
                return data.get("response", "").strip()
                
        except Exception as e:
            self.logger.error(f"Error generating response: {e}")
            raise
    
    async def is_available(self) -> bool:
        """Check if Ollama service is available."""
        try:
            session = await self._get_session()
            async with session.get(f"{self.base_url}/api/tags") as response:
                return response.status == 200
        except Exception as e:
            self.logger.error(f"Ollama service unavailable: {e}")
            return False
    
    async def close(self):
        """Close the HTTP session."""
        if self.session and not self.session.closed:
            await self.session.close()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
