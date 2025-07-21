"""
Model information structure for the application.
"""
from typing import Optional
from pydantic import BaseModel

class LLMModelInfo(BaseModel):
    """Information about a llm model."""
    name: str
    size: Optional[str] = None
    modified_at: Optional[str] = None
