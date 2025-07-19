"""
Application configuration management.
This provides type-safe configuration with environment variable support.
"""
import os
from typing import Optional
from pydantic import BaseModel, Field


class Settings(BaseModel):
    """Application settings with environment variable support."""
    
    # Server settings
    app_name: str = "AI Local Comp Backend"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Ollama settings
    ollama_url: str = "http://localhost:11434"
    
    # Model settings
    router_model: str = "phi:latest"
    code_model: str = "codellama:instruct"
    simple_model: str = "mistral:instruct"
    complex_model: str = "llama3:instruct"
    
    # Router settings
    use_langchain_router: bool = False
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "backend.log"
    
    def __init__(self, **kwargs):
        # Override with environment variables
        env_overrides = {
            'debug': os.getenv('DEBUG', 'false').lower() == 'true',
            'host': os.getenv('HOST', '0.0.0.0'),
            'port': int(os.getenv('PORT', '8000')),
            'ollama_url': os.getenv('OLLAMA_URL', 'http://localhost:11434'),
            'router_model': os.getenv('ROUTER_MODEL', 'phi:latest'),
            'code_model': os.getenv('CODE_MODEL', 'codellama:instruct'),
            'simple_model': os.getenv('SIMPLE_MODEL', 'mistral:instruct'),
            'complex_model': os.getenv('COMPLEX_MODEL', 'llama3:instruct'),
            'use_langchain_router': os.getenv('USE_LANGCHAIN_ROUTER', 'false').lower() == 'true',
            'log_level': os.getenv('LOG_LEVEL', 'INFO'),
            'log_file': os.getenv('LOG_FILE', 'backend.log'),
        }
        
        # Merge kwargs with env overrides
        merged_data = {**kwargs, **env_overrides}
        super().__init__(**merged_data)


# Global settings instance
settings = Settings()
