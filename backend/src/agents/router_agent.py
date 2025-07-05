from src.config import load_config
from src.agents.langchain_router_agent import LangchainRouterAgent
from src.agents.ollama_agent import OllamaAgent
from src.agents.default.code_agent import CodeAgent
from src.agents.default.fast_agent import FastAgent
from src.agents.default.general_agent import GeneralAgent
import logging

logger = logging.getLogger(__name__)

class RouterAgent:
    def __init__(self):
        cfg = load_config()
        self.use_langchain_router = cfg.get("use_langchain_router", False)
        self.langchain_router = LangchainRouterAgent()
        self.router_model = cfg["router_model"]
        self.code_model = cfg["code_model"]
        self.simple_model = cfg["simple_model"]
        self.complex_model = cfg["complex_model"]
        self.ollama_url = cfg["ollama_url"]
        self.router = OllamaAgent(self.router_model, self.ollama_url)
        self.code_agent = CodeAgent(self.code_model, self.ollama_url)
        self.fast_agent = FastAgent(self.simple_model, self.ollama_url)
        self.general_agent = GeneralAgent(self.complex_model, self.ollama_url)

    def decide_agent(self, user_prompt: str) -> str:
        routing_prompt = (
            'Choose which agent should respond to the following query.\n\n'
            f'Query:\n"""{user_prompt}"""\n\n'
            'Respond with exactly one word:\n'
            '- "code" → if it\'s a programming-related question.\n'
            '- "simple" → if it\'s a quick general fact or easy question.\n'
            '- "complex" → if it\'s nuanced, abstract, or multi-part.\n\n'
            'Your answer:'
        )
        answer = self.router.generate(routing_prompt).lower()
        logger.info(f"[INTERN ROUTER] Routing decision: '{answer}' for prompt: {user_prompt}")
        if "code" in answer:
            return "code"
        elif "simple" in answer:
            return "simple"
        else:
            return "complex"

    def run(self, prompt: str) -> dict:
        cfg = load_config()
        use_langchain = cfg.get("use_langchain_router", False)
        if use_langchain:
            logger.info(f"[LANGCHAIN ROUTER] Routing with LangChain for prompt: {prompt}")
            return self.langchain_router.run(prompt)
        else:
            agent_type = self.decide_agent(prompt)
            logger.info(f"[INTERN ROUTER] Using agent: {agent_type} for prompt: {prompt}")
            if agent_type == "code":
                response = self.code_agent.generate(prompt)
                model_used = self.code_model
            elif agent_type == "simple":
                response = self.fast_agent.generate(prompt)
                model_used = self.simple_model
            else:
                response = self.general_agent.generate(prompt)
                model_used = self.complex_model
            return {"response": response, "model": model_used}
