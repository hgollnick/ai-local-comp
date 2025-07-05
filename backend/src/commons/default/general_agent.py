from ..ollama_service import OllamaAgent

class GeneralAgent(OllamaAgent):
    def __init__(self, model, ollama_url):
        super().__init__(model, ollama_url)
