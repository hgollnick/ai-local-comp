import requests
import logging
import os
from typing import List

logger = logging.getLogger(__name__)

def list_models() -> List[str]:
    ollama_url = os.environ.get("OLLAMA_URL", "http://localhost:11434")
    try:
        response = requests.get(f"{ollama_url}/api/tags")
        response.raise_for_status()
        data = response.json()
        # The models are under the "models" key, each with a "name"
        return [model["name"] for model in data.get("models", [])]
    except Exception as e:
        logger.error(f"Error fetching models: {e}")
        return []

def pull_model(model_name: str) -> requests.Response:
    """Call Ollama's /api/pull endpoint to pull a model."""
    ollama_url = os.environ.get("OLLAMA_URL", "http://localhost:11434")
    response = requests.post(f"{ollama_url}/api/pull", json={"name": model_name}, stream=True)
    return response