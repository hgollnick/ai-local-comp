from ..ollama_agent import OllamaAgent

class FastAgent(OllamaAgent):
    def __init__(self, model, ollama_url):
        super().__init__(model, ollama_url)
