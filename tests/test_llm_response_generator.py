# Tests for LLM response generator

import pytest
from unittest.mock import Mock, MagicMock
from agents.llm_response_generator import LLMResponseGenerator
from agents.schema import TicketResponse


class TestLLMResponseGenerator:
    @pytest.fixture
    def mock_client(self):
        """Create mock OpenAI client"""
        mock = Mock()
        mock.chat_completion.return_value = MagicMock(
            choices=[
                MagicMock(
                    message=MagicMock(
                        content='{"response_text": "Thank you for contacting us about your password reset. Here are the steps...", "citations": ["KB-001"], "quality_score": 0.85, "needs_human_review": false}'
                    )
                )
            ]
        )
        return mock

    def test_generate_password_reset_response(self, mock_client):
        """Test response generation for password reset"""
        generator = LLMResponseGenerator(mock_client)
        result = generator.generate(
            "I forgot my password",
            "password_reset",
            ["KB-001: Password Reset Guide"]
        )

        assert result.response_text is not None
        assert len(result.response_text) > 20
        assert "KB-001" in result.citations
        assert result.quality_score == 0.85
        assert result.needs_human_review is False

    def test_generate_billing_response(self, mock_client):
        """Test response generation for billing inquiry"""
        mock_client.chat_completion.return_value.choices[0].message.content = (
            '{"response_text": "Thank you for reaching out about your billing question. Let me look into this for you...", "citations": ["KB-002"], "quality_score": 0.75, "needs_human_review": false}'
        )

        generator = LLMResponseGenerator(mock_client)
        result = generator.generate(
            "I was charged twice",
            "billing_inquiry",
            ["KB-002: Billing Support"]
        )

        assert result.response_text is not None
        assert result.quality_score == 0.75
        assert result.needs_human_review is False

    def test_generate_low_quality_response(self, mock_client):
        """Test low quality response needs human review"""
        mock_client.chat_completion.return_value.choices[0].message.content = (
            '{"response_text": "Test", "citations": [], "quality_score": 0.5, "needs_human_review": true}'
        )

        generator = LLMResponseGenerator(mock_client)
        result = generator.generate("Test", "general_inquiry")

        assert result.quality_score == 0.5
        assert result.needs_human_review is True  # Should be overridden

    def test_generate_fallback_on_error(self):
        """Test fallback response on API failure"""
        mock_client = Mock()
        mock_client.chat_completion.side_effect = Exception("API Error")

        generator = LLMResponseGenerator(mock_client)
        result = generator.generate("Test", "general_inquiry")

        assert "support agent" in result.response_text.lower()
        assert result.needs_human_review is True
        assert result.quality_score == 0.5

    def test_evaluate_quality_short_response(self, mock_client):
        """Test quality evaluation for short response"""
        generator = LLMResponseGenerator(mock_client)
        quality = generator.evaluate_quality("Short")

        assert quality == 0.0  # Too short

    def test_evaluate_quality_good_response(self, mock_client):
        """Test quality evaluation for good response"""
        generator = LLMResponseGenerator(mock_client)
        quality = generator.evaluate_quality("Thank you for contacting us. We are happy to help you with your inquiry. Please provide more details.")

        assert quality > 0.5

    def test_should_human_review_threshold(self, mock_client):
        """Test human review threshold"""
        generator = LLMResponseGenerator(mock_client)

        assert generator.should_human_review(0.6) is True
        assert generator.should_human_review(0.7) is False
        assert generator.should_human_review(0.8) is False
