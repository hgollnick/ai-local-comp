"""
Model-related request and response schemas.
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class ModelsResponse(BaseModel):
    """Response schema for listing available models."""
    models: List[str] = Field(
        ..., 
        description="List of available model names"
    )
    count: Optional[int] = Field(
        None,
        description="Total number of models"
    )

    def __init__(self, **data):
        super().__init__(**data)
        if self.count is None:
            self.count = len(self.models)

    class Config:
        json_schema_extra = {
            "example": {
                "models": ["llama3:instruct", "codellama:instruct", "mistral:instruct"],
                "count": 3
            }
        }


class PullModelRequest(BaseModel):
    """Request schema for pulling a model."""
    model_name: str = Field(
        ...,
        description="Name of the model to pull",
        example="llama3:instruct"
    )
    force: bool = Field(
        False,
        description="Force pull even if model exists"
    )


class PullModelResponse(BaseModel):
    """Response schema for model pull operations."""
    status: str = Field(
        ...,
        description="Status of the pull operation"
    )
    message: str = Field(
        ...,
        description="Detailed message about the operation"
    )
    model_name: str = Field(
        ...,
        description="Name of the model that was pulled"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "message": "Model llama3:instruct pulled successfully",
                "model_name": "llama3:instruct"
            }
        }
