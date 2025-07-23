#!/usr/bin/env python3
"""
Entry point for the application.
Supports both production and debug modes.
"""
import uvicorn
from app.main import app
from app.core.config import settings

if __name__ == "__main__":
    # Check if we're in debug mode
    if settings.debug:
        print("🐛 DEBUG MODE ENABLED")
        print(f"📊 Server: http://{settings.host}:{settings.port}")
        print(f"📚 Docs: http://{settings.host}:{settings.port}/docs")
        print("🔄 Auto-reload: ON")
        print("=" * 50)
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
        access_log=settings.debug
    )
