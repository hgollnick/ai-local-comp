"""
Agent services for handling different types of requests.
"""
import time
from typing import Dict, Any, Optional
from enum import Enum

from app.services.base import AgentService
from app.services.ollama_sync import OllamaService
from app.core.config import settings
from app.models.agent import AgentResponse


class AgentType(str, Enum):
    """Types of agents available."""
    CODE = "code"
    SIMPLE = "simple"
    COMPLEX = "complex"


class RouterService(AgentService):
    """Service for routing requests to appropriate agents."""
    
    def __init__(self):
        super().__init__()
        self.router_service = OllamaService(settings.router_model)
    
    async def classify_request(self, prompt: str) -> AgentType:
        """Classify the request to determine which agent to use."""
        routing_prompt = (
            'Choose which agent should respond to the following query.\n\n'
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
                return AgentType.CODE
            elif "simple" in answer:
                return AgentType.SIMPLE
            else:
                return AgentType.COMPLEX
                
        except Exception as e:
            self.logger.error(f"Error in routing: {e}")
            return AgentType.COMPLEX  # Default fallback
    
    async def process(self, prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process request by routing to appropriate agent."""
        start_time = time.time()
        
        try:
            # Classify the request
            agent_type = await self.classify_request(prompt)
            
            # Get the appropriate agent
            agent_service = self._get_agent_service(agent_type)
            
            # Process the request
            response = await agent_service.process(prompt, context)
            
            processing_time = time.time() - start_time
            response["processing_time"] = processing_time
            response["agent_type"] = agent_type.value
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error processing request: {e}")
            processing_time = time.time() - start_time
            return {
                "response": f"Error processing request: {str(e)}",
                "model": "error",
                "agent_type": "error",
                "processing_time": processing_time
            }
    
    def _get_agent_service(self, agent_type: AgentType) -> AgentService:
        """Get the appropriate agent service based on type."""
        if agent_type == AgentType.CODE:
            return CodeAgentService()
        elif agent_type == AgentType.SIMPLE:
            return SimpleAgentService()
        else:
            return ComplexAgentService()


class CodeAgentService(AgentService):
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
                "agent_type": AgentType.CODE.value
            }
        except Exception as e:
            self.logger.error(f"Error in code agent: {e}")
            raise


class SimpleAgentService(AgentService):
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
                "agent_type": AgentType.SIMPLE.value
            }
        except Exception as e:
            self.logger.error(f"Error in simple agent: {e}")
            raise


class ComplexAgentService(AgentService):
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
                "agent_type": AgentType.COMPLEX.value
            }
        except Exception as e:
            self.logger.error(f"Error in complex agent: {e}")
            raise
