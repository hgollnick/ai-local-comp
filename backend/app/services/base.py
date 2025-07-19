"""
Base service class and interfaces.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseService(ABC):
    """Base service class for all services."""
    
    def __init__(self):
        self.logger = self._get_logger()
    
    def _get_logger(self):
        """Get logger for the service."""
        import logging
        return logging.getLogger(f"app.services.{self.__class__.__name__}")


class LLMService(BaseService):
    """Base class for LLM services."""
    
    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate response from LLM."""
        pass
    
    @abstractmethod
    async def is_available(self) -> bool:
        """Check if the LLM service is available."""
        pass


class AgentService(BaseService):
    """Base class for agent services."""
    
    @abstractmethod
    async def process(self, prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process a request and return response."""
        pass
