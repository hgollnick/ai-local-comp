"""
Dependency injection utilities and providers.
Following FastAPI dependency injection patterns for clean architecture.
"""
import logging
from functools import lru_cache
from typing import AsyncGenerator

from app.services.selector.basic_model_selector import BasicModelSelectorService
from app.services.selector.langchain_model_selector import LangchainModelSelector
from app.services.llm_models import LLMModelService
from app.core.config import Settings, settings
from app.services.base import ModelSelector

logger = logging.getLogger("app.dependencies")


async def get_router_service() -> AsyncGenerator[ModelSelector, None]:
    """
    Get router service instance with proper cleanup.
    
    This dependency provides a RouterService instance and ensures
    proper resource cleanup after the request is completed.
    """
    import app.services.config as config_service
    cfg = config_service.load_config()
    if cfg.get("use_langchain_router"):
        service = LangchainModelSelector()
    else:
        service = BasicModelSelectorService()
    try:
        yield service
    finally:
        # Cleanup if needed (e.g., close connections)
        if hasattr(service, 'close'):
            await service.close()


async def get_model_service() -> AsyncGenerator[LLMModelService, None]:
    """
    Get model service instance with proper cleanup.
    
    This dependency provides a ModelService instance and ensures
    proper resource cleanup after the request is completed.
    """
    service = LLMModelService()
    try:
        yield service
    finally:
        # Ensure cleanup
        await service.close()


def get_logger(name: str = "app") -> logging.Logger:
    """
    Get a logger instance for the specified module.
    
    Args:
        name: Logger name, typically the module name
        
    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)
