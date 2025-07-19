"""
Unit tests for Ollama service.
Tests the OllamaService class in isolation.
"""
import pytest
from unittest.mock import AsyncMock, Mock, patch
import aiohttp

from app.services.ollama import OllamaService
from app.core.config import settings


class TestOllamaService:
    """Test cases for OllamaService."""
    
    def test_initialization(self):
        """Test service initialization with default and custom values."""
        # Test with defaults
        service = OllamaService("test-model")
        assert service.model == "test-model"
        assert service.base_url == settings.ollama_url
        
        # Test with custom base_url
        service = OllamaService("test-model", "http://custom:11434")
        assert service.base_url == "http://custom:11434"
    
    @pytest.mark.asyncio
    async def test_generate_success(self):
        """Test successful response generation."""
        service = OllamaService("test-model")
        
        # Mock the session and response
        mock_response = Mock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={
            "response": "Test response from model"
        })
        
        mock_session = Mock()
        mock_session.post.return_value.__aenter__.return_value = mock_response
        
        with patch.object(service, '_get_session', return_value=mock_session):
            result = await service.generate("Test prompt")
            
            assert result == "Test response from model"
            mock_session.post.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_generate_http_error(self):
        """Test handling of HTTP errors during generation."""
        service = OllamaService("test-model")
        
        mock_response = Mock()
        mock_response.status = 500
        mock_response.text = AsyncMock(return_value="Internal server error")
        
        mock_session = Mock()
        mock_session.post.return_value.__aenter__.return_value = mock_response
        
        with patch.object(service, '_get_session', return_value=mock_session):
            with pytest.raises(Exception) as exc_info:
                await service.generate("Test prompt")
            
            assert "Ollama API error 500" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_is_available_success(self):
        """Test successful availability check."""
        service = OllamaService("test-model")
        
        mock_response = Mock()
        mock_response.status = 200
        
        mock_session = Mock()
        mock_session.get.return_value.__aenter__.return_value = mock_response
        
        with patch.object(service, '_get_session', return_value=mock_session):
            result = await service.is_available()
            
            assert result is True
    
    @pytest.mark.asyncio
    async def test_is_available_failure(self):
        """Test availability check failure."""
        service = OllamaService("test-model")
        
        mock_session = Mock()
        mock_session.get.side_effect = aiohttp.ClientError("Connection failed")
        
        with patch.object(service, '_get_session', return_value=mock_session):
            result = await service.is_available()
            
            assert result is False
    
    @pytest.mark.asyncio
    async def test_context_manager(self):
        """Test async context manager functionality."""
        service = OllamaService("test-model")
        
        async with service:
            assert service is not None
        
        # Verify close was called (if session exists)
        # This would need more sophisticated mocking in a real scenario
