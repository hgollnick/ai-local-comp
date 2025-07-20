"""
Domain models for the application.
"""
from typing import Dict, Any, Optional
from pydantic import BaseModel


class AgentResponse(BaseModel):
    """Response from an agent."""
    response: str
    model: str
    agent_type: str
    processing_time: Optional[float] = None


class AgentRequest(BaseModel):
    """Request to an agent."""
    prompt: str
    context: Optional[Dict[str, Any]] = None




