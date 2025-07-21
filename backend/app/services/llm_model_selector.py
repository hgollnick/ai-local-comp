"""
LLMModel services for handling different types of requests.
"""
import time
from typing import Dict, Any
from enum import Enum

from app.services.base import ModelSelector
from app.services.ollama.ollama_sync import OllamaService
from app.core.config import settings
from app.services import config as config_service


class LLMModelType(str, Enum):
    """Types of llms available."""
    CODE = "code"
    SIMPLE = "simple"
    COMPLEX = "complex"


class LLMModelSelectorService(ModelSelector):
    """Service for routing requests to appropriate LLM Model."""
    
    def __init__(self):
        super().__init__()
        self.router_service = OllamaService(config_service.load_config().get("router_model"))
    
    async def classify_request(self, prompt: str) -> LLMModelType:
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
                return LLMModelType.CODE
            elif "simple" in answer:
                return LLMModelType.SIMPLE
            else:
                return LLMModelType.COMPLEX
                
        except Exception as e:
            self.logger.error(f"Error in routing: {e}")
            return LLMModelType.COMPLEX  # Default fallback
    
    async def process(self, prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process request by routing to appropriate model."""
        start_time = time.time()
        
        try:
            # Classify the request
            llm_model_type = await self.classify_request(prompt)
            
            # Get the appropriate model
            model_service = self._get_model_service(llm_model_type)
            
            # Process the request
            response = await model_service.process(prompt, context)
            
            processing_time = time.time() - start_time
            response["processing_time"] = processing_time
            response["llm_model_type"] = llm_model_type.value
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error processing request: {e}")
            processing_time = time.time() - start_time
            return {
                "response": f"Error processing request: {str(e)}",
                "model": "error",
                "llm_model_type": "error",
                "processing_time": processing_time
            }
    
    def _get_model_service(self, llm_model_type: LLMModelType) -> ModelSelector:
        """Get the appropriate model service based on type."""
        if llm_model_type == LLMModelType.CODE:
            return CodeModelService()
        elif llm_model_type == LLMModelType.SIMPLE:
            return SimpleModelService()
        else:
            return ComplexModelService()


class CodeModelService(ModelSelector):
    """Service for handling code-related requests."""
    
    def __init__(self):
        super().__init__()
        self.ollama_service = OllamaService(settings.code_model)
    
    async def process(self, prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process code-related requests."""
        try:
            enhanced_prompt = f"You are a coding assistant. Provide code or technical help for: {prompt}"
            response = await self.ollama_service.generate(enhanced_prompt)
            
            return {
                "response": response,
                "model": settings.code_model,
                "llm_model_type": LLMModelType.CODE.value
            }
        except Exception as e:
            self.logger.error(f"Error in code model: {e}")
            raise


class SimpleModelService(ModelSelector):
    """Service for handling simple requests."""
    
    def __init__(self):
        super().__init__()
        self.ollama_service = OllamaService(settings.simple_model)
    
    async def process(self, prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process simple requests."""
        try:
            enhanced_prompt = f"Answer this question simply and concisely: {prompt}"
            response = await self.ollama_service.generate(enhanced_prompt)
            
            return {
                "response": response,
                "model": settings.simple_model,
                "llm_model_type": LLMModelType.SIMPLE.value
            }
        except Exception as e:
            self.logger.error(f"Error in simple model: {e}")
            raise


class ComplexModelService(ModelSelector):
    """Service for handling complex requests."""
    
    def __init__(self):
        super().__init__()
        self.ollama_service = OllamaService(settings.complex_model)
    
    async def process(self, prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process complex requests."""
        try:
            enhanced_prompt = f"You are a general assistant. Answer the following comprehensively: {prompt}"
            response = await self.ollama_service.generate(enhanced_prompt)
            
            return {
                "response": response,
                "model": settings.complex_model,
                "llm_model_type": LLMModelType.COMPLEX.value
            }
        except Exception as e:
            self.logger.error(f"Error in complex model: {e}")
            raise
