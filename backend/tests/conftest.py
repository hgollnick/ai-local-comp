"""
Test configuration and shared fixtures.
Provides common test utilities and mocks for the entire test suite.
"""
import pytest
import asyncio
from unittest.mock import AsyncMock, Mock
from typing import AsyncGenerator, Generator

from fastapi.testclient import TestClient
from app.main import app
from app.services.agents import RouterService
from app.services.models import ModelService
from app.services.ollama import OllamaService


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def client() -> TestClient:
    """
    Test client fixture for integration tests.
    
    Provides a TestClient instance for testing FastAPI endpoints.
    """
    return TestClient(app)


@pytest.fixture
def mock_ollama_service() -> Mock:
    """
    Mock OllamaService fixture.
    
    Provides a mocked OllamaService instance with common responses.
    """
    service = Mock(spec=OllamaService)
    service.generate = AsyncMock(return_value="Mocked response")
    service.is_available = AsyncMock(return_value=True)
    service.close = AsyncMock()
    return service


@pytest.fixture
def mock_router_service() -> Mock:
    """
    Mock RouterService fixture.
    
    Provides a mocked RouterService instance for testing agent routing.
    """
    service = Mock(spec=RouterService)
    service.process = AsyncMock(return_value={
        "response": "Test response from router",
        "model": "test-model",
        "agent_type": "test",
        "processing_time": 0.1
    })
    service.classify_request = AsyncMock(return_value="simple")
    service.close = AsyncMock()
    return service


@pytest.fixture
def mock_model_service() -> Mock:
    """
    Mock ModelService fixture.
    
    Provides a mocked ModelService instance for testing model operations.
    """
    service = Mock(spec=ModelService)
    service.list_models = AsyncMock(return_value=[
        "llama3:instruct", 
        "codellama:instruct", 
        "mistral:instruct",
        "phi:latest"
    ])
    service.pull_model = AsyncMock(return_value={
        "status": "success",
        "message": "Model pulled successfully"
    })
    service.model_exists = AsyncMock(return_value=False)
    service.close = AsyncMock()
    return service


@pytest.fixture
def sample_ask_request() -> dict:
    """
    Sample ask request fixture.
    
    Provides sample request data for testing ask endpoints.
    """
    return {
        "prompt": "What is the capital of France?",
        "context": {
            "language": "en",
            "type": "factual"
        }
    }


@pytest.fixture
def sample_ask_response() -> dict:
    """
    Sample ask response fixture.
    
    Provides sample response data for testing.
    """
    return {
        "response": "The capital of France is Paris.",
        "model": "mistral:instruct",
        "router": "intern",
        "agent_type": "simple",
        "processing_time": 0.85
    }


@pytest.fixture
def sample_models_list() -> list:
    """
    Sample models list fixture.
    
    Provides a sample list of available models for testing.
    """
    return [
        "llama3:instruct",
        "codellama:instruct", 
        "mistral:instruct",
        "phi:latest",
        "gemma:7b"
    ]


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "unit: mark test as unit test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
