"""
Configuration API endpoints.
Handles application configuration management.
"""

import logging
from app.services import config as config_service
from fastapi import APIRouter
from app.schemas.config import ConfigResponse
from app.core.config import settings
from app.models.selector_config import SelectorConfig

logger = logging.getLogger("app.api.config")
router = APIRouter(prefix="/config", tags=["configuration"])


@router.get("/", response_model=ConfigResponse)
@router.get("", response_model=ConfigResponse)  # Handle both with and without trailing slash
async def get_config() -> ConfigResponse:
    """
    Get current application configuration from config.json.
    """
    logger.info("Fetching current configuration from file")
    cfg = config_service.load_config()
    return ConfigResponse(**cfg)


# POST endpoint to save configuration
@router.post("/", response_model=dict)
@router.post("", response_model=dict)  # Handle both with and without trailing slash
async def set_config(cfg: SelectorConfig):
    """
    Save application configuration to a file.
    """
    config_service.save_config(cfg.model_dump())
    logger.info("Config saved.")
    return {"status": "ok"}
