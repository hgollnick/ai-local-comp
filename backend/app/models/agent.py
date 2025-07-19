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


class ModelInfo(BaseModel):
    """Information about a model."""
    name: str
    size: Optional[str] = None
    modified_at: Optional[str] = None


class ConfigModel(BaseModel):
    """Application configuration model."""
    router_model: str
    code_model: str
    simple_model: str
    complex_model: str
    ollama_url: str
    use_langchain_router: bool
