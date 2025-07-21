"""
API v1 router configuration.
Aggregates all v1 endpoints into a single router.
"""
from fastapi import APIRouter

from app.api.v1.endpoints import config, health, logs, ollama

# Create the v1 router
router = APIRouter()

# Include all endpoint routers
router.include_router(health.router)
router.include_router(ollama.router) 
router.include_router(config.router)
router.include_router(logs.router)