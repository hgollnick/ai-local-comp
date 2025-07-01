import os
import requests

class OllamaAgent:
    def __init__(self, model, ollama_url=None):
        self.model = model
        self.ollama_url = ollama_url or os.environ.get("OLLAMA_URL", "http://localhost:11434")

    def generate(self, prompt: str) -> str:
        print(f"[OllamaAgent] Using model: {self.model}")
        print(f"[OllamaAgent] Using endpoint: {self.ollama_url}/api/generate")
        print(f"[OllamaAgent] Prompt: {prompt}")
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                }
            )
            print(f"[OllamaAgent] Ollama response status: {response.status_code}")
            print(f"[OllamaAgent] Ollama response body: {response.text}")
            response.raise_for_status()
            return response.json()["response"].strip()
        except Exception as e:
            print(f"[OllamaAgent] Exception: {e}")
            raise
