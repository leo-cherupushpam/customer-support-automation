# Tests for streaming response generation

import pytest
from unittest.mock import Mock, patch, MagicMock
from agents.llm_response_generator_streaming import LLMResponseGeneratorStreaming


class TestLLMResponseGeneratorStreaming:
    """Test streaming response generation"""

    @pytest.fixture
    def mock_client(self):
        """Create mock OpenAI client with streaming"""
        mock = Mock()
        
        # Create mock streaming response
        mock_stream = MagicMock()
        mock_stream.__iter__ = Mock(return_value=iter([
            MagicMock(choices=[MagicMock(delta=MagicMock(content="Thank"))]),
            MagicMock(choices=[MagicMock(delta=MagicMock(content=" you"))]),
            MagicMock(choices=[MagicMock(delta=MagicMock(content=" for"))]),
            MagicMock(choices=[MagicMock(delta=MagicMock(content=" contacting"))]),
            MagicMock(choices=[MagicMock(delta=MagicMock(content=" us."))]),
        ]))
        
        mock.chat_completion.return_value = mock_stream
        return mock

    def test_streaming_response_generation(self, mock_client):
        """Test that streaming generates responses token by token"""
        generator = LLMResponseGeneratorStreaming(mock_client)
        
        # Collect streamed tokens
        collected_tokens = []
        for token in generator.stream_response("Test ticket", "password_reset"):
            collected_tokens.append(token)
        
        # Verify tokens were streamed
        assert len(collected_tokens) > 0
        assert "Thank" in collected_tokens[0]
        assert "us." in collected_tokens[-1]
        
        # Verify full response
        full_response = "".join(collected_tokens)
        assert "Thank you for contacting us." in full_response

    def test_streaming_empty_response(self, mock_client):
        """Test streaming with empty response"""
        mock_stream = MagicMock()
        mock_stream.__iter__ = Mock(return_value=iter([
            MagicMock(choices=[MagicMock(delta=MagicMock(content=""))]),
        ]))
        mock_client.chat_completion.return_value = mock_stream
        
        generator = LLMResponseGeneratorStreaming(mock_client)
        tokens = list(generator.stream_response("Test", "general"))
        
        assert len(tokens) >= 1

    def test_streaming_with_context(self, mock_client):
        """Test streaming with KB context"""
        generator = LLMResponseGeneratorStreaming(mock_client)
        
        tokens = list(generator.stream_response(
            "I forgot my password",
            "password_reset",
            kb_articles=["KB-001: Password Reset Guide"]
        ))
        
        assert len(tokens) > 0

    def test_streaming_error_handling(self):
        """Test streaming error handling"""
        mock_client = Mock()
        mock_client.chat_completion.side_effect = Exception("API Error")
        
        generator = LLMResponseGeneratorStreaming(mock_client)
        
        # Should handle error gracefully
        tokens = list(generator.stream_response("Test", "general"))
        
        # Should return empty list or fallback
        assert isinstance(tokens, list)
