from fastapi import APIRouter
from app.services.logs import stream_logs_service

router = APIRouter(prefix="/logs", tags=["logs"])

@router.get("/stream")
def stream_logs():
    """Endpoint to stream logs using the service."""
    return stream_logs_service()
