"""
Configuration-related schemas.
"""
from typing import Optional
from pydantic import BaseModel, Field


class ConfigResponse(BaseModel):
    """Response schema for configuration data."""
    router_model: str = Field(
        ...,
        description="Model used for request routing"
    )
    code_model: str = Field(
        ...,
        description="Model used for code-related questions"
    )
    simple_model: str = Field(
        ...,
        description="Model used for simple questions"
    )
    complex_model: str = Field(
        ...,
        description="Model used for complex questions"
    )
    ollama_url: str = Field(
        ...,
        description="URL of the Ollama service"
    )
    use_langchain_router: bool = Field(
        ...,
        description="Whether to use LangChain router instead of internal"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "router_model": "phi:latest",
                "code_model": "codellama:instruct",
                "simple_model": "mistral:instruct", 
                "complex_model": "llama3:instruct",
                "ollama_url": "http://localhost:11434",
                "use_langchain_router": False
            }
        }


class ConfigUpdateRequest(BaseModel):
    """Request schema for updating configuration."""
    router_model: Optional[str] = Field(
        None,
        description="Model used for request routing"
    )
    code_model: Optional[str] = Field(
        None,
        description="Model used for code-related questions"
    )
    simple_model: Optional[str] = Field(
        None,
        description="Model used for simple questions"
    )
    complex_model: Optional[str] = Field(
        None,
        description="Model used for complex questions"
    )
    ollama_url: Optional[str] = Field(
        None,
        description="URL of the Ollama service"
    )
    use_langchain_router: Optional[bool] = Field(
        None,
        description="Whether to use LangChain router instead of internal"
    )
