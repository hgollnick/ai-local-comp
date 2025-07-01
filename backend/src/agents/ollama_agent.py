import requests

class OllamaAgent:
    def __init__(self, model, ollama_url=None):
        self.model = model
        self.ollama_url = ollama_url or "http://localhost:11434"

    def generate(self, prompt: str) -> str:
        response = requests.post(
            f"{self.ollama_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
        )
        response.raise_for_status()
        return response.json()["response"].strip()
