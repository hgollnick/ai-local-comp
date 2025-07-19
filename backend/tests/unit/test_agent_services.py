"""
Unit tests for agent services.
Tests business logic in isolation with mocked dependencies.
"""
import pytest
from unittest.mock import AsyncMock, Mock, patch
from typing import Dict, Any

from app.services.agents import (
    RouterService, 
    CodeAgentService, 
    SimpleAgentService, 
    ComplexAgentService,
    AgentType
)


class TestRouterService:
    """Test cases for RouterService business logic."""
    
    @pytest.mark.asyncio
    async def test_classify_request_code_keywords(self):
        """Test classification identifies code-related keywords."""
        with patch.object(RouterService, '_get_agent_service'):
            with patch('app.services.ollama.OllamaService.generate', new_callable=AsyncMock) as mock_generate:
                mock_generate.return_value = "code"
                
                service = RouterService()
                result = await service.classify_request("How do I write a Python function?")
                
                assert result == AgentType.CODE
                mock_generate.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_classify_request_simple_question(self):
        """Test classification identifies simple factual questions."""
        with patch.object(RouterService, '_get_agent_service'):
            with patch('app.services.ollama.OllamaService.generate', new_callable=AsyncMock) as mock_generate:
                mock_generate.return_value = "simple"
                
                service = RouterService()
                result = await service.classify_request("What is the capital of France?")
                
                assert result == AgentType.SIMPLE
    
    @pytest.mark.asyncio
    async def test_classify_request_complex_analysis(self):
        """Test classification identifies complex analytical questions."""
        with patch.object(RouterService, '_get_agent_service'):
            with patch('app.services.ollama.OllamaService.generate', new_callable=AsyncMock) as mock_generate:
                mock_generate.return_value = "complex"
                
                service = RouterService()
                result = await service.classify_request("Analyze the implications of quantum computing on cryptography")
                
                assert result == AgentType.COMPLEX
    
    @pytest.mark.asyncio
    async def test_classify_request_error_fallback(self):
        """Test classification falls back to complex on errors."""
        with patch.object(RouterService, '_get_agent_service'):
            with patch('app.services.ollama.OllamaService.generate', new_callable=AsyncMock) as mock_generate:
                mock_generate.side_effect = Exception("Connection error")
                
                service = RouterService()
                result = await service.classify_request("Any question")
                
                assert result == AgentType.COMPLEX
    
    @pytest.mark.asyncio
    async def test_process_returns_complete_response(self):
        """Test process method returns all required response fields."""
        with patch.object(RouterService, 'classify_request', new_callable=AsyncMock) as mock_classify:
            with patch.object(RouterService, '_get_agent_service') as mock_get_agent:
                
                mock_classify.return_value = AgentType.CODE
                mock_agent = Mock()
                mock_agent.process = AsyncMock(return_value={
                    "response": "Test response",
                    "model": "test-model",
                    "agent_type": "code"
                })
                mock_get_agent.return_value = mock_agent
                
                service = RouterService()
                result = await service.process("Test prompt")
                
                assert "response" in result
                assert "model" in result
                assert "agent_type" in result
                assert "processing_time" in result
                assert result["agent_type"] == "code"


class TestCodeAgentService:
    """Test cases for CodeAgentService."""
    
    @pytest.mark.asyncio
    async def test_process_enhances_prompt_for_coding(self):
        """Test that code agent enhances prompts with coding context."""
        with patch('app.services.ollama.OllamaService.generate', new_callable=AsyncMock) as mock_generate:
            mock_generate.return_value = "def hello(): print('Hello')"
            
            service = CodeAgentService()
            result = await service.process("Write a hello function")
            
            # Verify the prompt was enhanced for coding
            call_args = mock_generate.call_args[0][0]
            assert "coding assistant" in call_args.lower()
            assert "technical help" in call_args.lower()
            
            assert result["response"] == "def hello(): print('Hello')"
            assert result["agent_type"] == AgentType.CODE.value


class TestSimpleAgentService:
    """Test cases for SimpleAgentService."""
    
    @pytest.mark.asyncio
    async def test_process_requests_concise_response(self):
        """Test that simple agent requests concise responses."""
        with patch('app.services.ollama.OllamaService.generate', new_callable=AsyncMock) as mock_generate:
            mock_generate.return_value = "Paris"
            
            service = SimpleAgentService()
            result = await service.process("What is the capital of France?")
            
            # Verify the prompt was enhanced for simplicity
            call_args = mock_generate.call_args[0][0]
            assert "simply and concisely" in call_args.lower()
            
            assert result["response"] == "Paris"
            assert result["agent_type"] == AgentType.SIMPLE.value


class TestComplexAgentService:
    """Test cases for ComplexAgentService."""
    
    @pytest.mark.asyncio
    async def test_process_requests_comprehensive_response(self):
        """Test that complex agent requests comprehensive responses."""
        with patch('app.services.ollama.OllamaService.generate', new_callable=AsyncMock) as mock_generate:
            mock_generate.return_value = "Quantum computing uses quantum mechanical phenomena..."
            
            service = ComplexAgentService()
            result = await service.process("Explain quantum computing")
            
            # Verify the prompt was enhanced for comprehensive analysis
            call_args = mock_generate.call_args[0][0]
            assert "comprehensively" in call_args.lower()
            
            assert result["agent_type"] == AgentType.COMPLEX.value
