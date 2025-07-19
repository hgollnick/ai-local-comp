"""
Common schemas used across the application.
"""
from typing import Optional
from pydantic import BaseModel, Field


class StatusResponse(BaseModel):
    """Generic status response schema."""
    status: str = Field(
        ..., 
        description="Status of the operation or service"
    )
    message: Optional[str] = Field(
        None, 
        description="Additional message or details"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "message": "Operation completed successfully"
            }
        }


class ErrorResponse(BaseModel):
    """Error response schema."""
    error: str = Field(
        ..., 
        description="Error message"
    )
    detail: Optional[str] = Field(
        None, 
        description="Detailed error information"
    )
    code: Optional[str] = Field(
        None, 
        description="Error code for programmatic handling"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "error": "Validation failed",
                "detail": "The provided input did not pass validation",
                "code": "VALIDATION_ERROR"
            }
        }
