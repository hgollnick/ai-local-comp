import json
import logging
from langchain_community.llms import Ollama
from langchain.chains import MultiPromptChain, LLMChain
from langchain.chains.router import LLMRouterChain
from langchain.chains.router.llm_router import RouterOutputParser
from langchain.prompts import PromptTemplate
from langchain.schema import OutputParserException
from src.config import load_config

class LangchainRouterAgent:
    def __init__(self):
        # Setup logging
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        
        cfg = load_config()
        self.ollama_url = cfg["ollama_url"]
        self.router_model = cfg["router_model"]
        self.code_model = cfg["code_model"]
        self.simple_model = cfg["simple_model"]
        self.complex_model = cfg["complex_model"]

        # LLMs
        router_llm = Ollama(model=self.router_model, base_url=self.ollama_url)
        code_llm = Ollama(model=self.code_model, base_url=self.ollama_url)
        simple_llm = Ollama(model=self.simple_model, base_url=self.ollama_url)
        complex_llm = Ollama(model=self.complex_model, base_url=self.ollama_url)

        # Prompts with proper router setup
        router_prompt = PromptTemplate(
            input_variables=["input"],
            template="""You are a router for a multi-model assistant. Given a user input, select the best prompt name from: code, simple, complex.

Return a markdown code block with a JSON object:
```json
{
  "destination": <prompt name or 'DEFAULT'>,
  "next_inputs": <possibly modified input>
}
```

Choose 'code' for programming, 'simple' for quick facts, 'complex' for general/complex questions.

User input: {input}"""
        )
        
        # Add the RouterOutputParser
        router_prompt.output_parser = RouterOutputParser()
        
        code_prompt = PromptTemplate(
            input_variables=["input"],
            template="You are a code assistant. Answer the following: {input}"
        )
        simple_prompt = PromptTemplate(
            input_variables=["input"],
            template="You are a fast fact assistant. Answer the following: {input}"
        )
        complex_prompt = PromptTemplate(
            input_variables=["input"],
            template="You are a general assistant. Answer the following: {input}"
        )

        # Chains
        self.router_chain = LLMRouterChain.from_llm(
            llm=router_llm,
            prompt=router_prompt
        )
        self.destination_chains = {
            "code": LLMChain(llm=code_llm, prompt=code_prompt),
            "simple": LLMChain(llm=simple_llm, prompt=simple_prompt),
            "complex": LLMChain(llm=complex_llm, prompt=complex_prompt),
        }
        self.default_chain = self.destination_chains["complex"]

        self.chain = MultiPromptChain(
            router_chain=self.router_chain,
            destination_chains=self.destination_chains,
            default_chain=self.default_chain,
            verbose=True,
        )

    def _sanitize_router_output(self, output: str) -> str:
        """Sanitize router output to extract JSON if wrapped in code block or malformed."""
        import re
        self.logger.debug(f"Raw router output: {output}")
        match = re.search(r'```json(.*?)```', output, re.DOTALL)
        if match:
            return match.group(1).strip()
        return output.strip()

    def run(self, prompt: str) -> str:
        try:
            self.logger.info(f"Running router agent for input: {prompt}")
            result = self.chain.invoke({"input": prompt})
            self.logger.info(f"Chain result: {result}")
            return result
        except OutputParserException as e:
            self.logger.error(f"Router output parsing failed: {e}")
            # Try to sanitize and re-parse if possible
            try:
                sanitized = self._sanitize_router_output(str(e))
                self.logger.info(f"Sanitized router output: {sanitized}")
                # Optionally, try to parse JSON here or return fallback
                return f"[Router output parse error, sanitized output: {sanitized}]"
            except Exception as inner_e:
                self.logger.error(f"Sanitization failed: {inner_e}")
                return "[Router output parse error, unable to sanitize output]"
        except Exception as ex:
            self.logger.error(f"Unhandled exception in router agent: {ex}")
            return "[Router agent error: see logs for details]"