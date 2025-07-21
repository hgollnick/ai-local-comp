"""
Dependency injection utilities and providers.
Following FastAPI dependency injection patterns for clean architecture.
"""
import logging
from functools import lru_cache
from typing import AsyncGenerator

from app.services.llm_model_selector import LLMModelSelectorService
from app.services.llm_models import LLMModelService
from app.core.config import Settings, settings

logger = logging.getLogger("app.dependencies")


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Using lru_cache ensures we create only one instance of settings
    throughout the application lifecycle.
    """
    return settings


async def get_router_service() -> AsyncGenerator[LLMModelSelectorService, None]:
    """
    Get router service instance with proper cleanup.
    
    This dependency provides a RouterService instance and ensures
    proper resource cleanup after the request is completed.
    """
    service = LLMModelSelectorService()
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
