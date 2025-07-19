"""
Tests for services.
"""
import pytest
from unittest.mock import AsyncMock, Mock, patch

from app.services.agents import RouterService, AgentType
from app.services.ollama import OllamaService


class TestRouterService:
    """Test cases for RouterService."""
    
    @pytest.mark.asyncio
    async def test_classify_request_code(self):
        """Test classification of code-related requests."""
        with patch.object(OllamaService, 'generate', new_callable=AsyncMock) as mock_generate:
            mock_generate.return_value = "code"
            
            service = RouterService()
            result = await service.classify_request("How do I write a for loop in Python?")
            
            assert result == AgentType.CODE
    
    @pytest.mark.asyncio
    async def test_classify_request_simple(self):
        """Test classification of simple requests."""
        with patch.object(OllamaService, 'generate', new_callable=AsyncMock) as mock_generate:
            mock_generate.return_value = "simple"
            
            service = RouterService()
            result = await service.classify_request("What is the capital of France?")
            
            assert result == AgentType.SIMPLE
    
    @pytest.mark.asyncio
    async def test_classify_request_complex(self):
        """Test classification of complex requests."""
        with patch.object(OllamaService, 'generate', new_callable=AsyncMock) as mock_generate:
            mock_generate.return_value = "complex"
            
            service = RouterService()
            result = await service.classify_request("Explain quantum computing")
            
            assert result == AgentType.COMPLEX
    
    @pytest.mark.asyncio
    async def test_classify_request_fallback(self):
        """Test fallback to complex for unrecognized responses."""
        with patch.object(OllamaService, 'generate', new_callable=AsyncMock) as mock_generate:
            mock_generate.return_value = "unknown"
            
            service = RouterService()
            result = await service.classify_request("Test question")
            
            assert result == AgentType.COMPLEX


class TestOllamaService:
    """Test cases for OllamaService."""
    
    @pytest.mark.asyncio
    @patch('aiohttp.ClientSession.post')
    async def test_generate_success(self, mock_post):
        """Test successful generation."""
        # Mock the response
        mock_response = Mock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={"response": "Test response"})
        mock_post.return_value.__aenter__.return_value = mock_response
        
        service = OllamaService("test-model")
        result = await service.generate("Test prompt")
        
        assert result == "Test response"
    
    @pytest.mark.asyncio
    @patch('aiohttp.ClientSession.get')
    async def test_is_available_success(self, mock_get):
        """Test availability check success."""
        mock_response = Mock()
        mock_response.status = 200
        mock_get.return_value.__aenter__.return_value = mock_response
        
        service = OllamaService("test-model")
        result = await service.is_available()
        
        assert result is True
    
    @pytest.mark.asyncio
    @patch('aiohttp.ClientSession.get')
    async def test_is_available_failure(self, mock_get):
        """Test availability check failure."""
        mock_get.side_effect = Exception("Connection error")
        
        service = OllamaService("test-model")
        result = await service.is_available()
        
        assert result is False
