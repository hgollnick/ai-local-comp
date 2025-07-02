import logging
from langchain_community.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from src.config import load_config


class LangchainRouterAgent:
    def __init__(self):
        # Setup logging
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

        # Load config
        cfg = load_config()
        self.ollama_url = cfg["ollama_url"]
        self.complex_model = cfg["complex_model"]
        self.simple_model = cfg.get("simple_model", self.complex_model)
        self.code_model = cfg.get("code_model", self.complex_model)

        # Initialize LLMs and chains
        self.complex_chain = LLMChain(
            llm=Ollama(model=self.complex_model, base_url=self.ollama_url),
            prompt=PromptTemplate(
                input_variables=["input"],
                template="You are a general assistant. Answer the following: {input}"
            )
        )
        self.simple_chain = LLMChain(
            llm=Ollama(model=self.simple_model, base_url=self.ollama_url),
            prompt=PromptTemplate(
                input_variables=["input"],
                template="Answer this question simply and concisely: {input}"
            )
        )
        self.code_chain = LLMChain(
            llm=Ollama(model=self.code_model, base_url=self.ollama_url),
            prompt=PromptTemplate(
                input_variables=["input"],
                template="You are a coding assistant. Provide code or technical help for: {input}"
            )
        )

    def route(self, prompt: str) -> str:
        # Simple routing logic: can be replaced with more advanced classification
        code_keywords = ["code", "python", "function", "class", "bug", "error", "script", "algorithm", "implement", "write a program", "write code", "fix this"]
        simple_keywords = ["what is", "who is", "define", "explain", "when is", "where is", "how many", "list", "name"]
        prompt_lower = prompt.lower()
        if any(kw in prompt_lower for kw in code_keywords):
            return "code"
        elif any(kw in prompt_lower for kw in simple_keywords) and len(prompt.split()) < 15:
            return "simple"
        else:
            return "complex"

    def run(self, prompt: str) -> str:
        self.logger.info(f"Running agent for input: {prompt}")
        try:
            route = self.route(prompt)
            self.logger.info(f"Routing to: {route}")
            if route == "simple":
                result = self.simple_chain.invoke({"input": prompt})
            elif route == "code":
                result = self.code_chain.invoke({"input": prompt})
            else:
                result = self.complex_chain.invoke({"input": prompt})
            self.logger.info(f"Final response: {result}")
            return result
        except Exception as e:
            self.logger.error(f"Agent failed: {e}")
            return f"[Agent error: {e}]"
