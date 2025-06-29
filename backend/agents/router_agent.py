from functools import lru_cache
from backend.config import load_config
from backend.agents.ollama_agent import OllamaAgent
from backend.agents.code_agent import CodeAgent
from backend.agents.fast_agent import FastAgent
from backend.agents.general_agent import GeneralAgent


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
        routing_prompt = self._build_routing_prompt(user_prompt)
        answer = self.router.generate(routing_prompt).lower()
        return self._parse_routing_answer(answer)

    def _build_routing_prompt(self, user_prompt: str) -> str:
        return (
            'Choose which agent should respond to the following query.\n\n'
            f'Query:\n"""{user_prompt}"""\n\n'
            'Respond with exactly one word:\n'
            '- "code" → if it\'s a programming-related question.\n'
            '- "simple" → if it\'s a quick general fact or easy question.\n'
            '- "complex" → if it\'s nuanced, abstract, or multi-part.\n\n'
            'Your answer:'
        )

    def _parse_routing_answer(self, answer: str) -> str:
        if "code" in answer:
            return "code"
        elif "simple" in answer:
            return "simple"
        else:
            return "complex"

    def run(self, prompt: str) -> str:
        agent_type = self.decide_agent(prompt)
        if agent_type == "code":
            return self.code_agent.generate(prompt)
        elif agent_type == "simple":
            return self.fast_agent.generate(prompt)
        else:
            return self.general_agent.generate(prompt)
