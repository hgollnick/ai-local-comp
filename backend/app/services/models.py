"""
Service for managing Ollama models.
"""
from typing import List, Dict, Any
import requests
import json

from app.services.base import BaseService
from app.core.config import settings


class ModelService(BaseService):
    """Service for managing Ollama models."""
    
    def __init__(self):
        super().__init__()
        self.base_url = settings.ollama_url
        self.timeout = 300  # 5 minutes for model pulling
    
    async def list_models(self) -> List[str]:
        """Get list of available models from Ollama."""
        self.logger.info(f"Fetching models from {self.base_url}/api/tags")
        
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            if response.status_code != 200:
                raise Exception(f"Failed to fetch models: {response.status_code} {response.text}")
            
            data = response.json()
            models = [model["name"] for model in data.get("models", [])]
            
            self.logger.debug(f"Models fetched: {models}")
            return models
                
        except Exception as e:
            self.logger.error(f"Error fetching models: {e}")
            return []
    
    async def pull_model(self, model_name: str) -> Dict[str, Any]:
        """Pull a model from Ollama registry."""
        self.logger.info(f"Pulling model '{model_name}' from {self.base_url}/api/pull")
        
        try:
            payload = {"name": model_name}
            
            response = requests.post(
                f"{self.base_url}/api/pull",
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code != 200:
                raise Exception(f"Failed to pull model: {response.status_code} {response.text}")
            
            return {
                "status": "success",
                "message": f"Model {model_name} pulled successfully"
            }
                
        except Exception as e:
            self.logger.error(f"Error pulling model {model_name}: {e}")
            raise
    
    async def model_exists(self, model_name: str) -> bool:
        """Check if a model exists locally."""
        try:
            models = await self.list_models()
            return model_name in models
        except Exception as e:
            self.logger.error(f"Error checking if model exists: {e}")
            return False
    
    async def close(self):
        """No-op for requests-based implementation."""
        pass
