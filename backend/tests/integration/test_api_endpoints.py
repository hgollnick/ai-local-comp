"""
Integration tests for API endpoints.
Tests the full request/response cycle with real FastAPI app.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

from app.main import app


@pytest.fixture
def client():
    """Test client for integration tests."""
    return TestClient(app)


class TestHealthEndpoints:
    """Integration tests for health check endpoints."""
    
    def test_root_endpoint(self, client):
        """Test root endpoint returns correct response."""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "running"
        assert "AI Local Comp Backend" in data["message"]
    
    def test_health_check(self, client):
        """Test basic health check endpoint."""
        response = client.get("/api/v1/health/")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "running" in data["message"]
    
    def test_readiness_check(self, client):
        """Test readiness check endpoint."""
        response = client.get("/api/v1/health/readiness")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "ready"
    
    def test_liveness_check(self, client):
        """Test liveness check endpoint."""
        response = client.get("/api/v1/health/liveness")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "alive"


class TestConfigEndpoints:
    """Integration tests for configuration endpoints."""
    
    def test_get_config(self, client):
        """Test configuration retrieval."""
        response = client.get("/api/v1/config/")
        assert response.status_code == 200
        
        data = response.json()
        required_fields = [
            "router_model", "code_model", "simple_model", 
            "complex_model", "ollama_url", "use_langchain_router"
        ]
        for field in required_fields:
            assert field in data


class TestAgentEndpoints:
    """Integration tests for agent endpoints."""
    
    @patch("app.dependencies.get_router_service")
    def test_ask_question_success(self, mock_get_service, client):
        """Test successful question processing."""
        # Mock the service
        mock_service = AsyncMock()
        mock_service.process.return_value = {
            "response": "This is a test response",
            "model": "test-model",
            "agent_type": "simple",
            "processing_time": 0.5
        }
        mock_get_service.return_value.__aenter__.return_value = mock_service
        
        request_data = {
            "prompt": "What is 2+2?",
            "context": {"type": "math"}
        }
        
        response = client.post("/api/v1/agents/ask", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["response"] == "This is a test response"
        assert data["model"] == "test-model"
        assert data["agent_type"] == "simple"
        assert data["processing_time"] == 0.5
    
    def test_ask_question_validation_error(self, client):
        """Test validation error handling."""
        # Empty prompt should fail validation
        request_data = {"prompt": ""}
        
        response = client.post("/api/v1/agents/ask", json=request_data)
        assert response.status_code == 422  # Validation error
    
    def test_ask_question_missing_prompt(self, client):
        """Test missing prompt field."""
        request_data = {"context": {"type": "test"}}
        
        response = client.post("/api/v1/agents/ask", json=request_data)
        assert response.status_code == 422  # Validation error


class TestModelEndpoints:
    """Integration tests for model endpoints."""
    
    @patch("app.dependencies.get_model_service")
    def test_list_models_success(self, mock_get_service, client):
        """Test successful model listing."""
        mock_service = AsyncMock()
        mock_service.list_models.return_value = [
            "llama3:instruct", "codellama:instruct", "mistral:instruct"
        ]
        mock_service.close = AsyncMock()
        mock_get_service.return_value.__aenter__.return_value = mock_service
        
        response = client.get("/api/v1/models/")
        assert response.status_code == 200
        
        data = response.json()
        assert "models" in data
        assert len(data["models"]) == 3
        assert "count" in data
        assert data["count"] == 3
    
    @patch("app.dependencies.get_model_service")
    def test_pull_model_success(self, mock_get_service, client):
        """Test successful model pulling."""
        mock_service = AsyncMock()
        mock_service.model_exists.return_value = False
        mock_service.pull_model.return_value = {"status": "success"}
        mock_service.close = AsyncMock()
        mock_get_service.return_value.__aenter__.return_value = mock_service
        
        response = client.post("/api/v1/models/pull/test-model")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "success"
        assert data["model_name"] == "test-model"
    
    @patch("app.dependencies.get_model_service")  
    def test_pull_existing_model(self, mock_get_service, client):
        """Test pulling a model that already exists."""
        mock_service = AsyncMock()
        mock_service.model_exists.return_value = True
        mock_service.close = AsyncMock()
        mock_get_service.return_value.__aenter__.return_value = mock_service
        
        response = client.post("/api/v1/models/pull/existing-model")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "success"
        assert "already exists" in data["message"]
