from functools import lru_cache
import requests
from .config import load_config
from .agents.ollama_agent import OllamaAgent
from .agents.code_agent import CodeAgent
from .agents.fast_agent import FastAgent
from .agents.general_agent import GeneralAgent
from .agents.router_agent import RouterAgent

# Base model runner
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

# 🚀 Router agent using smallest available model (cached)
class RouterAgent:
    def __init__(self):
        cfg = load_config()
        self.router_model = cfg["router_model"]
        self.code_model = cfg["code_model"]
        self.simple_model = cfg["simple_model"]
        self.complex_model = cfg["complex_model"]
        self.ollama_url = cfg["ollama_url"]

        self.router = OllamaAgent(self.router_model, self.ollama_url)
        self.code_agent = CodeAgent(self.code_model, self.ollama_url)
        self.fast_agent = FastAgent(self.simple_model, self.ollama_url)
        self.general_agent = GeneralAgent(self.complex_model, self.ollama_url)

    @lru_cache(maxsize=100)
    def decide_agent(self, user_prompt: str) -> str:
        routing_prompt = f"""Choose which agent should respond to the following query.

Query:
\"\"\"{user_prompt}\"\"\"

Respond with exactly one word:
- "code" → if it's a programming-related question.
- "simple" → if it's a quick general fact or easy question.
- "complex" → if it's nuanced, abstract, or multi-part.

Your answer:"""

        answer = self.router.generate(routing_prompt).lower()
        if "code" in answer:
            return "code"
        elif "simple" in answer:
            return "simple"
        else:
            return "complex"

    def run(self, prompt: str) -> str:
        agent_type = self.decide_agent(prompt)
        print(f"🧭 Routing to: {agent_type} agent")
        if agent_type == "code":
            return self.code_agent.generate(prompt)
        elif agent_type == "simple":
            return self.fast_agent.generate(prompt)
        else:
            return self.general_agent.generate(prompt)

if __name__ == "__main__":
    router = RouterAgent()
    while True:
        user_prompt = input("🗨️ You: ")
        if user_prompt.lower() in ("exit", "quit"):
            break
        response = router.run(user_prompt)
        print(f"🤖 Assistant: {response}\n")