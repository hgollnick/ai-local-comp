import logging
import time
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
from app.services import config as config_service
from app.services.base import ModelSelector

class LangchainModelSelector(ModelSelector):
    """LangChain-based model selector."""
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        cfg = config_service.load_config()
        self.ollama_url = cfg["ollama_url"]
        self.router_model = cfg["router_model"]
        self.complex_model = cfg.get("complex_model", self.router_model)
        self.simple_model = cfg.get("simple_model", self.router_model)
        self.code_model = cfg.get("code_model", self.router_model)
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
        # Classification chain using LangChain
        from langchain_core.output_parsers import StrOutputParser
        from langchain_core.prompts import PromptTemplate as CorePromptTemplate
        self.classification_chain = (
            CorePromptTemplate.from_template(
                """Given the user question below, classify it as either `simple`, `complex`, or `code`.\n\nDo not respond with more than one word.\n\n<question>\n{question}\n</question>\n\nClassification:"""
            )
            | Ollama(model=self.router_model, base_url=self.ollama_url)
            | StrOutputParser()
        )
    def classify(self, prompt: str) -> str:
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
    def classify_request(self, prompt: str):
        return self.classify(prompt)

    async def process(self, prompt: str, context=None) -> dict:
        start_time = time.time()
        classification = self.classify_request(prompt)
        prompt_input = [prompt] if not isinstance(prompt, list) else prompt
        if classification == "simple":
            result = self.simple_chain.invoke({"input": prompt_input[0]})
            model_used = self.simple_model
        elif classification == "code":
            result = self.code_chain.invoke({"input": prompt_input[0]})
            model_used = self.code_model
        else:
            result = self.complex_chain.invoke({"input": prompt_input[0]})
            model_used = self.complex_model
        response_text = result["text"] if isinstance(result, dict) and "text" in result else result
        response = {
            "response": response_text,
            "model": model_used,
            "llm_model_type": classification,
            "processing_time": time.time() - start_time
        }
        return response
