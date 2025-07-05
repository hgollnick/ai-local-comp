from ..ollama_service import OllamaService

class CodeAgent(OllamaService):
    def __init__(self, model, ollama_url):
        super().__init__(model, ollama_url)
