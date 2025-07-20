"""
Configuration API endpoints.
Handles application configuration management.
"""
import logging
from fastapi import APIRouter, HTTPException

from app.schemas.config import ConfigResponse
from app.core.config import settings
from app.models.config import ConfigModel
import json

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


# POST endpoint to save configuration
@router.post("/", response_model=dict)
async def set_config(cfg: ConfigModel):
    """
    Save application configuration to a file.
    """
    logger.info(f"POST /config called with: {cfg}")
    with open("config.json", "w") as f:
        json.dump(cfg.model_dump(), f, indent=2)
    logger.info("Config saved.")
    return {"status": "ok"}
