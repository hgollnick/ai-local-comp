#!/usr/bin/env python3
"""
Debug helper script for development.
Provides various debugging utilities and modes.
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
    # Load debug environment
    env_debug = Path(__file__).parent / ".env.debug"
    if env_debug.exists():
        with open(env_debug) as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
    
    # Set debug logging
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
    
    from fastapi.testclient import TestClient
    from app.main import app
    
    client = TestClient(app)
    
    print("🧪 Testing API endpoints...")
    
    # Test health
    print("\n1. Testing health endpoint:")
    response = client.get("/api/v1/health/")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    # Test config
    print("\n2. Testing config endpoint:")
    response = client.get("/api/v1/config/")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    # Test models (if Ollama is running)
    print("\n3. Testing models endpoint:")
    try:
        response = client.get("/api/v1/models/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test ask endpoint
    print("\n4. Testing ask endpoint:")
    try:
        response = client.post("/api/v1/agents/ask", json={
            "prompt": "What is 2+2?",
            "context": {"type": "math"}
        })
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")

def debug_services():
    """Debug individual services."""
    setup_debug_environment()
    
    print("🔧 Testing services...")
    
    # Test config loading
    print("\n1. Testing configuration:")
    from app.core.config import settings
    print(f"   App name: {settings.app_name}")
    print(f"   Debug mode: {settings.debug}")
    print(f"   Ollama URL: {settings.ollama_url}")
    
    # Test Ollama service
    print("\n2. Testing Ollama service:")
    import asyncio
    from app.services.ollama_sync import OllamaService
    
    async def test_ollama():
        service = OllamaService("phi:latest")
        try:
            available = await service.is_available()
            print(f"   Ollama available: {available}")
            
            if available:
                response = await service.generate("Hello")
                print(f"   Test response: {response[:100]}...")
        except Exception as e:
            print(f"   Error: {e}")
    
    asyncio.run(test_ollama())

def main():
    """Main debug script."""
    parser = argparse.ArgumentParser(description="Debug helper for AI Local Comp Backend")
    parser.add_argument(
        "command",
        choices=["app", "test", "services", "all", "help"],
        help="Debug command to run"
    )
    
    args = parser.parse_args()
    
    if args.command == "help":
        print("🐛 AI Local Comp Backend Debug Helper")
        print("=" * 50)
        print("Commands:")
        print("  app      - Start debug server")
        print("  test     - Test API endpoints")
        print("  services - Test individual services")
        print("  all      - Run all tests")
        print()
        print("VS Code Debug Configurations:")
        print("  'Debug FastAPI App'        - Quick debugging (recommended)")
        print("  'Debug FastAPI with Uvicorn' - Server behavior debugging")
        print("  'Debug Tests'              - Debug test suite")
        print("  'Remote Debug'             - Attach to running process")
        print()
        print("💡 For most debugging, use 'Debug FastAPI App' configuration")
        return
    elif args.command == "app":
        debug_app()
    elif args.command == "test":
        debug_test_endpoints()
    elif args.command == "services":
        debug_services()
    elif args.command == "all":
        print("🚀 Running all debug tests...")
        debug_services()
        debug_test_endpoints()
        print("\n🎯 Tests complete. Run 'python debug.py app' to start debug server.")

if __name__ == "__main__":
    main()
