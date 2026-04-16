# Tests for LLM classifier

import pytest
from unittest.mock import Mock, patch, MagicMock
from agents.llm_classifier import LLMClassifier
from agents.schema import TicketClassification


class TestLLMClassifier:
    @pytest.fixture
    def mock_client(self):
        """Create mock OpenAI client"""
        mock = Mock()
        mock.chat_completion.return_value = MagicMock(
            choices=[
                MagicMock(
                    message=MagicMock(
                        content='{"category": "password_reset", "priority": 3, "sentiment": "neutral", "confidence": 0.9, "reasoning": "User asks to reset password"}'
                    )
                )
            ]
        )
        return mock

    def test_classify_password_reset(self, mock_client):
        """Test classification of password reset ticket"""
        classifier = LLMClassifier(mock_client)
        result = classifier.classify("I forgot my password, can you help me reset it?")

        assert result.category == "password_reset"
        assert result.priority == 3
        assert result.sentiment == "neutral"
        assert result.confidence == 0.9

    def test_classify_billing_inquiry(self, mock_client):
        """Test classification of billing inquiry"""
        mock_client.chat_completion.return_value.choices[0].message.content = (
            '{"category": "billing_inquiry", "priority": 4, "sentiment": "negative", "confidence": 0.85, "reasoning": "Customer mentions charges"}'
        )

        classifier = LLMClassifier(mock_client)
        result = classifier.classify("I was charged twice for my subscription")

        assert result.category == "billing_inquiry"
        assert result.priority == 4
        assert result.sentiment == "negative"

    def test_classify_feature_request(self, mock_client):
        """Test classification of feature request"""
        mock_client.chat_completion.return_value.choices[0].message.content = (
            '{"category": "feature_request", "priority": 2, "sentiment": "positive", "confidence": 0.8, "reasoning": "User suggests new feature"}'
        )

        classifier = LLMClassifier(mock_client)
        result = classifier.classify("Would love to see dark mode in the app")

        assert result.category == "feature_request"
        assert result.priority == 2
        assert result.sentiment == "positive"

    def test_classify_technical_issue(self, mock_client):
        """Test classification of technical issue"""
        mock_client.chat_completion.return_value.choices[0].message.content = (
            '{"category": "technical_issue", "priority": 5, "sentiment": "negative", "confidence": 0.95, "reasoning": "User reports bug"}'
        )

        classifier = LLMClassifier(mock_client)
        result = classifier.classify("The app keeps crashing when I try to upload files")

        assert result.category == "technical_issue"
        assert result.priority == 5
        assert result.sentiment == "negative"

    def test_classify_general_inquiry(self, mock_client):
        """Test classification of general inquiry"""
        mock_client.chat_completion.return_value.choices[0].message.content = (
            '{"category": "general_inquiry", "priority": 1, "sentiment": "neutral", "confidence": 0.7, "reasoning": "General question"}'
        )

        classifier = LLMClassifier(mock_client)
        result = classifier.classify("What are your business hours?")

        assert result.category == "general_inquiry"
        assert result.priority == 1

    def test_classify_with_low_confidence(self, mock_client):
        """Test handling of ambiguous tickets"""
        mock_client.chat_completion.return_value.choices[0].message.content = (
            '{"category": "general_inquiry", "priority": 2, "sentiment": "neutral", "confidence": 0.5, "reasoning": "Unclear ticket"}'
        )

        classifier = LLMClassifier(mock_client)
        result = classifier.classify("Something isn't working right")

        assert result.confidence == 0.5
        assert result.confidence < 0.7  # Low confidence

    def test_classify_fallback_on_error(self):
        """Test fallback to default classification on API failure"""
        mock_client = Mock()
        mock_client.chat_completion.side_effect = Exception("API Error")

        classifier = LLMClassifier(mock_client)
        result = classifier.classify("Test ticket")

        assert result.category == "general_inquiry"
        assert result.confidence == 0.5
        assert "API Error" in result.reasoning

    def test_classify_batch(self, mock_client):
        """Test batch classification"""
        mock_client.chat_completion.return_value.choices[0].message.content = (
            '{"category": "password_reset", "priority": 3, "sentiment": "neutral", "confidence": 0.9, "reasoning": "Test"}'
        )

        classifier = LLMClassifier(mock_client)
        tickets = ["Ticket 1", "Ticket 2", "Ticket 3"]
        results = classifier.classify_batch(tickets)

        assert len(results) == 3
        for result in results:
            assert result.category == "password_reset"
