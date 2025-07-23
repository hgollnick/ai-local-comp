"""
Application configuration management.
This provides type-safe configuration with environment variable support.
"""
import os
from pydantic import BaseModel


class Settings(BaseModel):
    """Application settings with environment variable support."""
    
    # Server settings
    app_name: str = "AI Local Comp Backend"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Ollama settings
    ollama_url: str = "http://localhost:11434"
    
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
            'log_level': os.getenv('LOG_LEVEL', 'INFO'),
            'log_file': os.getenv('LOG_FILE', 'backend.log'),
        }
        
        # Merge kwargs with env overrides
        merged_data = {**kwargs, **env_overrides}
        super().__init__(**merged_data)


# Global settings instance
settings = Settings()
