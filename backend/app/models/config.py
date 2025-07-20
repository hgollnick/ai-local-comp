"""
Configuration model for the application.
"""
from pydantic import BaseModel

class ConfigModel(BaseModel):
    """Application configuration model."""
    router_model: str
    code_model: str
    simple_model: str
    complex_model: str
    ollama_url: str
    use_langchain_router: bool
