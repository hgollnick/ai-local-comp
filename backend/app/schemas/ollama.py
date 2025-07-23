"""
Ollama-related request and response schemas.
"""
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    """Request schema for asking a question to Ollama."""
    prompt: str = Field(
        ..., 
        min_length=1, 
        max_length=10000,
        description="The question or prompt to ask",
        example="How do I write a for loop in Python?"
    )
    context: Optional[Dict[str, Any]] = Field(
        None, 
        description="Additional context for the request"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "prompt": "How do I write a for loop in Python?",
                "context": {"language": "python", "level": "beginner"}
            }
        }


class AskResponse(BaseModel):
    """Response schema for ollama interactions."""
    response: str = Field(
        ..., 
        description="Ollama's response to the question"
    )
    model: str = Field(
        ..., 
        description="The model used to generate the response"
    )
    model_selector: str = Field(
        ..., 
        description="The model selector used (langchain/basic)"
    )
    llm_model_type: str = Field(
        ..., 
        description="The type of model that handled the request"
    )
    processing_time: Optional[float] = Field(
        None, 
        description="Time taken to process the request in seconds"
    )

    class Config:
        protected_namespaces = ()
        json_schema_extra = {
            "example": {
                "response": "Here's how to write a for loop in Python: ...",
                "model": "codellama:instruct",
                "router": "intern",
                "llm_model_type": "code",
                "processing_time": 1.23
            }
        }
