"""
Health check and system status endpoints.
"""
import logging
from fastapi import APIRouter
from app.schemas.common import StatusResponse

logger = logging.getLogger("app.api.health")
router = APIRouter(prefix="/health", tags=["health"])


@router.get("/", response_model=StatusResponse)
@router.get("", response_model=StatusResponse)  # Handle both with and without trailing slash
async def health_check() -> StatusResponse:
    """
    Basic health check endpoint.
    
    Returns the current status of the service.
    """
    return StatusResponse(
        status="healthy", 
        message="AI Local Comp Backend is running"
    )


@router.get("/readiness", response_model=StatusResponse) 
async def readiness_check() -> StatusResponse:
    """
    Readiness check for container orchestration.
    
    Could be extended to check dependencies like Ollama availability.
    """
    return StatusResponse(
        status="ready",
        message="Service is ready to accept requests"
    )


@router.get("/liveness", response_model=StatusResponse)
async def liveness_check() -> StatusResponse:
    """
    Liveness check for container orchestration.
    """
    return StatusResponse(
        status="alive",
        message="Service is alive"
    )
