import logging
from langchain_community.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from src.config import load_config
# Add imports for classification chain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate as CorePromptTemplate


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
        # Add classification chain using Ollama
        self.classification_chain = (
            CorePromptTemplate.from_template(
                """Given the user question below, classify it as either `simple`, `complex`, or `code`.

Do not respond with more than one word.

<question>
{question}
</question>

Classification:"""
            )
            | Ollama(model=self.complex_model, base_url=self.ollama_url)
            | StrOutputParser()
        )

    def route(self, prompt: str) -> str:
        # Use classification chain to route
        try:
            classification = self.classification_chain.invoke({"question": prompt})
            classification = classification.strip().lower()
            if classification in ["simple", "complex", "code"]:
                return classification
            else:
                return "complex"
        except Exception as e:
            self.logger.error(f"Classification failed: {e}")
            return "complex"

    def run(self, prompt: str) -> dict:
        self.logger.info(f"Running agent for input: {prompt}")
        try:
            route = self.route(prompt)
            self.logger.info(f"Routing to: {route}")
            if route == "simple":
                result = self.simple_chain.invoke({"input": prompt})
                model_used = self.simple_model
            elif route == "code":
                result = self.code_chain.invoke({"input": prompt})
                model_used = self.code_model
            else:
                result = self.complex_chain.invoke({"input": prompt})
                model_used = self.complex_model
            self.logger.info(f"Final response: {result}")
            return {"response": result, "model": model_used}
        except Exception as e:
            self.logger.error(f"Agent failed: {e}")
            return {"response": f"[Agent error: {e}]", "model": None}
