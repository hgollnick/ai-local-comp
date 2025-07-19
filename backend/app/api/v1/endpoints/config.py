"""
Configuration API endpoints.
Handles application configuration management.
"""
import logging
from fastapi import APIRouter, HTTPException

from app.schemas.config import ConfigResponse
from app.core.config import settings

logger = logging.getLogger("app.api.config")
router = APIRouter(prefix="/config", tags=["configuration"])


@router.get("/", response_model=ConfigResponse)
async def get_config() -> ConfigResponse:
    """
    Get current application configuration.
    
    Returns the current model assignments and service settings.
    """
    logger.info("Fetching current configuration")
    
    return ConfigResponse(
        router_model=settings.router_model,
        code_model=settings.code_model,
        simple_model=settings.simple_model,
        complex_model=settings.complex_model,
        ollama_url=settings.ollama_url,
        use_langchain_router=settings.use_langchain_router
    )
