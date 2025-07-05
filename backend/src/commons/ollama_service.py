import os
import requests
import logging

logger = logging.getLogger(__name__)

class OllamaService:
    def __init__(self, model, ollama_url=None):
        self.model = model
        self.ollama_url = ollama_url or os.environ.get("OLLAMA_URL", "http://localhost:11434")
        logger.info(f"OllamaService initialized with model: {self.model}, endpoint: {self.ollama_url}")

    def generate(self, prompt: str) -> str:
        logger.info(f"[OllamaService] Using model: {self.model}")
        logger.info(f"[OllamaService] Using endpoint: {self.ollama_url}/api/generate")
        logger.info(f"[OllamaService] Prompt: {prompt}")
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                }
            )
            logger.info(f"[OllamaService] Ollama response status: {response.status_code}")
            logger.debug(f"[OllamaService] Ollama response body: {response.text}")
            response.raise_for_status()
            return response.json()["response"].strip()
        except Exception as e:
            logger.error(f"[OllamaService] Exception: {e}")
            raise
