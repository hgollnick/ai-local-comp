"""
Domain models for the application.
"""
from typing import Dict, Any, Optional
from pydantic import BaseModel


class LLMMessageResponse(BaseModel):
    """Response from an LLM."""
    response: str
    model_name: str
    llm_model_type: str
    
    processing_time: Optional[float] = None

    model_config = {'protected_namespaces': ()}


class LLMMessageRequest(BaseModel):
    """Request to an LLM."""
    prompt: str
    context: Optional[Dict[str, Any]] = None
    
    model_config = {'protected_namespaces': ()}
