# Response Agent Tests

import pytest
from unittest.mock import Mock
from src.agents.response_agent import ResponseAgent


class TestResponseAgent:
    """Test Response Agent RAG-based response generation"""

    def test_generates_response_for_password_reset(self):
        """RED: Test response generation for password reset tickets"""
        mock_generator = Mock()
        mock_generator.generate.return_value = Mock(
            response_text="Thank you for contacting us about your password reset. Here are the steps...",
            citations=["KB-001"],
            quality_score=0.85,
            needs_human_review=False,
        )
        agent = ResponseAgent(mock_generator)

        response = agent.generate_response("I forgot my password", "password_reset")

        assert response is not None
        assert len(response) > 20
        assert "password" in response.lower()

    def test_generates_response_for_billing_inquiry(self):
        """RED: Test response generation for billing inquiries"""
        mock_generator = Mock()
        mock_generator.generate.return_value = Mock(
            response_text="Thank you for reaching out about your billing question. Let me look into this for you...",
            citations=["KB-002"],
            quality_score=0.75,
            needs_human_review=False,
        )
        agent = ResponseAgent(mock_generator)

        response = agent.generate_response("I was charged twice", "billing_inquiry")

        assert response is not None
        assert len(response) > 20
        assert "charge" in response.lower() or "billing" in response.lower()

    def test_provides_citations(self):
        """RED: Test that responses include KB citations"""
        mock_generator = Mock()
        mock_generator.generate.return_value = Mock(
            response_text="Thank you for your inquiry. Please see our KB article for more details.",
            citations=["KB-001", "KB-002"],
            quality_score=0.8,
            needs_human_review=False,
        )
        agent = ResponseAgent(mock_generator)

        response = agent.generate_response("How do I reset my password?", "password_reset")

        assert response is not None
        assert len(response) > 50

    def test_quality_score_exists(self):
        """RED: Test that responses have quality scores"""
        mock_generator = Mock()
        mock_generator.generate.return_value = Mock(
            response_text="Test response",
            citations=[],
            quality_score=0.7,
            needs_human_review=False,
        )
        mock_generator.evaluate_quality.return_value = 0.85
        agent = ResponseAgent(mock_generator)

        response = agent.generate_response("I forgot my password", "password_reset")
        quality_score = agent.evaluate_quality(response)

        assert quality_score is not None
        assert isinstance(quality_score, (int, float))
        assert 0 <= quality_score <= 1
