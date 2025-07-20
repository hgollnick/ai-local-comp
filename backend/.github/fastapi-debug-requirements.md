# 🐛 FastAPI Debug Requirements & Setup Guide

A comprehensive guide for setting up debugging in FastAPI projects with VS Code.
This guide provides everything you need to debug FastAPI applications effectively.

## 📦 Debug Dependencies

```bash
# Core debugging requirements
debugpy>=1.8.0              # Python debugger for VS Code
uvicorn[standard]>=0.24.0   # ASGI server with full features

# Testing and debugging
pytest>=7.4.0               # Testing framework
pytest-asyncio>=0.21.0      # Async test support
httpx>=0.25.0                # HTTP client for testing FastAPI
pytest-cov>=4.1.0           # Coverage reporting

# Development tools
black>=23.0.0                # Code formatter
isort>=5.12.0                # Import sorter
flake8>=6.0.0                # Linting
mypy>=1.5.0                  # Type checking
pre-commit>=3.4.0            # Git hooks

# Optional but recommended
rich>=13.0.0                 # Better console output
ipython>=8.0.0               # Enhanced Python shell
watchdog>=3.0.0              # File watching for auto-reload
```

## 🔧 VS Code Debug Configuration

Create `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug FastAPI App",
            "type": "debugpy",
            "request": "launch",
            "program": "${workspaceFolder}/main.py",
            "console": "integratedTerminal",
            "env": {
                "DEBUG": "true",
                "LOG_LEVEL": "DEBUG",
                "PYTHONPATH": "${workspaceFolder}"
            },
            "jinja": true,
            "justMyCode": false
        },
        {
            "name": "Debug FastAPI with Uvicorn",
            "type": "debugpy",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "app.main:app",
                "--host", "0.0.0.0",
                "--port", "8000",
                "--log-level", "debug"
            ],
            "env": {
                "DEBUG": "true",
                "LOG_LEVEL": "DEBUG",
                "PYTHONPATH": "${workspaceFolder}"
            },
            "console": "integratedTerminal",
            "jinja": true,
            "justMyCode": false,
            "subProcess": true
        },
        {
            "name": "Debug Tests",
            "type": "debugpy",
            "request": "launch",
            "module": "pytest",
            "args": [
                "tests/",
                "-v",
                "--tb=short"
            ],
            "env": {
                "DEBUG": "true",
                "LOG_LEVEL": "DEBUG",
                "PYTHONPATH": "${workspaceFolder}"
            },
            "console": "integratedTerminal",
            "jinja": true,
            "justMyCode": false
        },
        {
            "name": "Remote Debug (debugpy)",
            "type": "debugpy",
            "request": "attach",
            "connect": {
                "host": "localhost",
                "port": 5678
            },
            "justMyCode": false
        }
    ]
}
```

## ⚙️ VS Code Settings

Create `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.terminal.activateEnvironment": true,
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests"],
    "python.testing.unittestEnabled": false,
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.mypyEnabled": true,
    "python.formatting.provider": "black",
    "python.sortImports.args": ["--profile", "black"],
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": "explicit"
    },
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        "**/.pytest_cache": true,
        "**/.mypy_cache": true
    },
    "python.envFile": "${workspaceFolder}/.env.debug"
}
```

## 🌱 Environment Configuration

Create `.env.debug`:

```bash
# Debug environment configuration
DEBUG=true
HOST=127.0.0.1
PORT=8000
LOG_LEVEL=DEBUG
LOG_FILE=debug.log

# Add your project-specific variables here
# DATABASE_URL=sqlite:///debug.db
# API_KEY=debug_key
```

## 🏗️ Application Structure for Debugging

### 1. Main Entry Point (`main.py`)

```python
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
```

### 2. FastAPI App with Debug Support (`app/main.py`)

```python
"""
Main FastAPI application with debug capabilities.
"""
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Optional debugpy support
try:
    import debugpy
    DEBUGPY_AVAILABLE = True
except ImportError:
    DEBUGPY_AVAILABLE = False

from app.core.config import settings
from app.core.logging import setup_logging

# Setup logging
logger = setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan with debug setup."""
    # Startup
    logger.info(f"Starting {settings.app_name}")
    logger.info(f"Debug mode: {settings.debug}")
    
    # Setup debugpy if in debug mode
    if settings.debug and DEBUGPY_AVAILABLE:
        try:
            debugpy.listen(("0.0.0.0", 5678))
            logger.info("Debugpy is listening on 0.0.0.0:5678")
        except Exception as e:
            logger.warning(f"Could not start debugpy: {e}")
    elif settings.debug and not DEBUGPY_AVAILABLE:
        logger.warning("Debug mode enabled but debugpy not available")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application")

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="Your FastAPI Application",
    version="1.0.0",
    lifespan=lifespan,
    debug=settings.debug  # Enable debug mode
)

# Add CORS middleware (configure for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.debug else ["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your routers here
# app.include_router(your_router, prefix="/api/v1")

@app.get("/")
async def root():
    """Root endpoint with debug info."""
    return {
        "message": f"Welcome to {settings.app_name}",
        "debug_mode": settings.debug,
        "docs_url": "/docs" if settings.debug else None
    }
```

### 3. Configuration with Debug Support (`app/core/config.py`)

```python
"""
Application configuration with debug support.
"""
import os
from pydantic import BaseModel

class Settings(BaseModel):
    """Application settings with environment variable support."""
    
    # Core settings
    app_name: str = "Your FastAPI App"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "app.log"
    
    def __init__(self, **kwargs):
        # Override with environment variables
        env_overrides = {
            'debug': os.getenv('DEBUG', 'false').lower() == 'true',
            'host': os.getenv('HOST', '0.0.0.0'),
            'port': int(os.getenv('PORT', '8000')),
            'log_level': os.getenv('LOG_LEVEL', 'INFO'),
            'log_file': os.getenv('LOG_FILE', 'app.log'),
        }
        
        # Add your custom env vars here
        # env_overrides['database_url'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
        
        merged_data = {**kwargs, **env_overrides}
        super().__init__(**merged_data)

# Global settings instance
settings = Settings()
```

### 4. Logging Configuration (`app/core/logging.py`)

```python
"""
Centralized logging configuration with debug support.
"""
import logging
import logging.config
from pathlib import Path
from app.core.config import settings

def setup_logging():
    """Configure application logging with debug support."""
    
    # Ensure log directory exists
    log_file = Path(settings.log_file)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Enhanced logging config for debugging
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "debug": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": settings.log_level,
                "formatter": "debug" if settings.debug else "default",
                "stream": "ext://sys.stdout",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": settings.log_level,
                "formatter": "debug" if settings.debug else "default",
                "filename": settings.log_file,
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
                "encoding": "utf8",
            },
        },
        "loggers": {
            "app": {
                "level": settings.log_level,
                "handlers": ["console", "file"],
                "propagate": False,
            },
            "uvicorn": {
                "level": "DEBUG" if settings.debug else "INFO",
                "handlers": ["console"],
                "propagate": False,
            },
        },
        "root": {
            "level": settings.log_level,
            "handlers": ["console", "file"],
        },
    }
    
    logging.config.dictConfig(logging_config)
    return logging.getLogger("app")
```

## 🧪 Debug Helper Script

Create `debug.py`:

```python
#!/usr/bin/env python3
"""
Debug helper script for FastAPI development.
"""
import argparse
import os
import sys
import logging
from pathlib import Path

# Add the app directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def setup_debug_environment():
    """Setup environment for debugging."""
    env_debug = Path(__file__).parent / ".env.debug"
    if env_debug.exists():
        with open(env_debug) as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
    
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )

def debug_app():
    """Run the application in debug mode."""
    setup_debug_environment()
    
    print("🐛 Starting FastAPI in DEBUG mode...")
    print("📝 Debug logging enabled")
    print("🔍 Breakpoints will work")
    print("🔄 Auto-reload enabled")
    print("=" * 50)
    
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="debug",
        access_log=True
    )

def debug_test_endpoints():
    """Test all endpoints interactively."""
    setup_debug_environment()
    
    try:
        from fastapi.testclient import TestClient
        from app.main import app
        
        client = TestClient(app)
        
        print("🧪 Testing API endpoints...")
        
        # Test root endpoint
        print("\n1. Testing root endpoint:")
        response = client.get("/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        # Add more endpoint tests here
        
    except ImportError as e:
        print(f"❌ Missing dependencies for testing: {e}")
        print("Install with: pip install httpx")

def main():
    """Main debug script."""
    parser = argparse.ArgumentParser(description="Debug helper for FastAPI")
    parser.add_argument(
        "command",
        choices=["app", "test"],
        help="Debug command to run"
    )
    
    args = parser.parse_args()
    
    if args.command == "app":
        debug_app()
    elif args.command == "test":
        debug_test_endpoints()

if __name__ == "__main__":
    main()
```

## 🚀 How to Use This Setup

### 1. **Copy Files to Your Project:**
```bash
# Copy the configuration files
cp .vscode/launch.json your-project/.vscode/
cp .vscode/settings.json your-project/.vscode/
cp .env.debug your-project/
cp debug.py your-project/
```

### 2. **Install Dependencies:**
```bash
pip install debugpy uvicorn[standard] pytest pytest-asyncio httpx
```

### 3. **Choose Your Debug Method:**

#### Method A: VS Code Debug (Recommended)
1. Open VS Code
2. Set breakpoints in your code
3. Press `F5` or go to Run & Debug
4. Choose "Debug FastAPI App" or "Debug FastAPI with Uvicorn"

#### Method B: Command Line Debug
```bash
# Quick debug
python debug.py app

# Test endpoints
python debug.py test
```

#### Method C: Remote Debug
1. Start your app with debugpy enabled
2. In VS Code, use "Remote Debug (debugpy)" configuration
3. Connect to localhost:5678

## 🎯 Debug Configuration Comparison

| Configuration | Use Case | When to Use |
|---------------|----------|-------------|
| **Debug FastAPI App** | Quick debugging | Business logic, services, configs |
| **Debug FastAPI with Uvicorn** | Server debugging | Middleware, request handling, performance |
| **Debug Tests** | Test debugging | Unit tests, integration tests |
| **Remote Debug** | Container debugging | Docker, remote servers |

## 🔍 Best Practices

1. **Always use `.env.debug`** for debug-specific settings
2. **Set `justMyCode: false`** to debug into libraries
3. **Use `DEBUG=true`** environment variable for debug mode
4. **Enable verbose logging** in debug mode
5. **Test both debug configurations** to understand differences
6. **Use breakpoints liberally** - they're free in debug mode
7. **Keep debug requirements separate** from production

## 📝 Customization Tips

- **Add project-specific env vars** to `.env.debug`
- **Modify logging format** for your needs
- **Add custom debug endpoints** for internal testing
- **Create debug-specific middleware** for request tracing
- **Use debug-only features** like detailed error pages

This setup provides comprehensive debugging capabilities for any FastAPI project! 🎉
