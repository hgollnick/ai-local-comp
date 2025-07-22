import time
from typing import Dict, Any
from enum import Enum
import logging

from app.services.base import ModelSelector
from app.services.ollama.ollama_sync import OllamaService
from app.core.config import settings
from app.services import config as config_service

cfg = config_service.load_config()

class BasicModelType(str, Enum):
    """Types of basic models available."""
    CODE = "code"
    SIMPLE = "simple"
    COMPLEX = "complex"

class BasicModelSelectorService(ModelSelector):
    """Service for routing requests to appropriate Basic Model."""
    def __init__(self):
        super().__init__()
        self.router_service = OllamaService(cfg.get("router_model"))

    async def classify_request(self, prompt: str):
        """Classify the request to determine which model to use."""
        routing_prompt = (
            'Choose which model should respond to the following query.\n\n'
            f'Query:\n"""{prompt}"""\n\n'
            'Respond with exactly one word:\n'
            '- "code" → if it\'s a programming-related question.\n'
            '- "simple" → if it\'s a quick general fact or easy question.\n'
            '- "complex" → if it\'s nuanced, abstract, or multi-part.\n\n'
            'Your answer:'
        )
        try:
            answer = await self.router_service.generate(routing_prompt)
            answer = answer.lower().strip()
            self.logger.info(f"Routing decision: '{answer}' for prompt: {prompt[:50]}...")
            if "code" in answer:
                return BasicModelType.CODE
            elif "simple" in answer:
                return BasicModelType.SIMPLE
            else:
                return BasicModelType.COMPLEX
        except Exception as e:
            self.logger.error(f"Error in routing: {e}")
            return BasicModelType.COMPLEX  # Default fallback

    async def process(self, prompt: str, context=None):
        """Process request by routing to appropriate model."""
        start_time = time.time()
        try:
            basic_model_type = await self.classify_request(prompt)
            model_service = self._get_model_service(basic_model_type)
            response = await model_service.process(prompt, context)
            processing_time = time.time() - start_time
            response["llm_model_type"] = basic_model_type.value
            response["processing_time"] = processing_time
            return response
        except Exception as e:
            self.logger.error(f"Error processing request: {e}")
            processing_time = time.time() - start_time
            return {
                "response": f"Error processing request: {str(e)}",
                "model": "error",
                "llm_model_type": "error",
                "processing_time": processing_time,
                "router": "error"
            }

    def _get_model_service(self, basic_model_type: BasicModelType) -> ModelSelector:
        """Get the appropriate model service based on type."""
        if basic_model_type == BasicModelType.CODE:
            return CodeModelService()
        elif basic_model_type == BasicModelType.SIMPLE:
            return SimpleModelService()
        else:
            return ComplexModelService()

class BaseModelService:
    """Base service for handling model requests."""
    def __init__(self, model_name, llm_model_type, enhanced_prompt_template):
        self.logger = logging.getLogger(__name__)
        self.ollama_service = OllamaService(model_name)
        self.llm_model_type = llm_model_type
        self.enhanced_prompt_template = enhanced_prompt_template

    async def process(self, prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        try:
            enhanced_prompt = self.enhanced_prompt_template.format(prompt=prompt)
            response = await self.ollama_service.generate(enhanced_prompt)
            return {
                "response": response,
                "model": self.ollama_service.model,
                "llm_model_type": self.llm_model_type
            }
        except Exception as e:
            self.logger.error(f"Error in {self.llm_model_type} model: {e}")
            raise

class CodeModelService(BaseModelService):
    def __init__(self):
        super().__init__(
            cfg.get("code_model"),
            BasicModelType.CODE.value,
            "You are a coding assistant. Provide code or technical help for: {prompt}"
        )

class SimpleModelService(BaseModelService):
    def __init__(self):
        super().__init__(
            cfg.get("simple_model"),
            BasicModelType.SIMPLE.value,
            "Answer this question simply and concisely: {prompt}"
        )

class ComplexModelService(BaseModelService):
    def __init__(self):
        super().__init__(
            cfg.get("complex_model"),
            BasicModelType.COMPLEX.value,
            "You are a general assistant. Answer the following comprehensively: {prompt}"
        )
