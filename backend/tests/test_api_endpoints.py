"""
Tests for API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


class TestAPIEndpoints:
    """Test cases for API endpoints."""
    
    def test_root_endpoint(self, client):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "status" in data
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_get_config(self, client):
        """Test get configuration endpoint."""
        response = client.get("/api/v1/config")
        assert response.status_code == 200
        data = response.json()
        assert "router_model" in data
        assert "code_model" in data
        assert "simple_model" in data
        assert "complex_model" in data
    
    @patch("app.api.endpoints.get_model_service")
    def test_get_models(self, mock_get_service, client, mock_model_service):
        """Test get models endpoint."""
        mock_get_service.return_value = mock_model_service
        
        response = client.get("/api/v1/models")
        assert response.status_code == 200
        data = response.json()
        assert "models" in data
        assert data["models"] == ["model1", "model2"]
    
    @patch("app.api.endpoints.get_router_service")
    def test_ask_question(self, mock_get_service, client, mock_router_service):
        """Test ask question endpoint."""
        mock_get_service.return_value = mock_router_service
        
        request_data = {"prompt": "What is Python?"}
        response = client.post("/api/v1/ask", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "model" in data
        assert "agent_type" in data
        assert data["response"] == "Test response"
    
    def test_ask_question_empty_prompt(self, client):
        """Test ask question with empty prompt."""
        request_data = {"prompt": ""}
        response = client.post("/api/v1/ask", json=request_data)
        assert response.status_code == 422  # Validation error
    
    @patch("app.api.endpoints.get_model_service")
    def test_pull_model(self, mock_get_service, client, mock_model_service):
        """Test pull model endpoint."""
        mock_get_service.return_value = mock_model_service
        
        response = client.post("/api/v1/pull_model/test-model")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
