"""
API v1 router configuration.
Aggregates all v1 endpoints into a single router.
"""
from fastapi import APIRouter

from app.api.v1.endpoints import agents, models, config, health

# Create the v1 router
router = APIRouter()

# Include all endpoint routers
router.include_router(health.router)
router.include_router(agents.router) 
router.include_router(models.router)
router.include_router(config.router)
