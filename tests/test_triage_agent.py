# Triage Agent Tests

import pytest
from unittest.mock import Mock
from src.agents.triage_agent import TriageAgent, ClassificationResult


class TestTriageAgent:
    """Test Triage Agent classification and confidence scoring"""

    def test_classifies_password_reset_ticket(self):
        """RED: Test that password reset tickets are classified correctly"""
        mock_classifier = Mock()
        mock_classifier.classify.return_value = Mock(
            category="password_reset",
            priority=3,
            sentiment="neutral",
            confidence=0.9,
            reasoning="Test",
        )
        agent = TriageAgent(mock_classifier)
        
        result = agent.classify_ticket("I forgot my password")

        assert result.category == "password_reset"
        assert result.confidence >= 0.85
        assert result.should_auto_respond() is True

    def test_classifies_billing_inquiry(self):
        """RED: Test billing inquiry classification"""
        mock_classifier = Mock()
        mock_classifier.classify.return_value = Mock(
            category="billing_inquiry",
            priority=4,
            sentiment="negative",
            confidence=0.75,
            reasoning="Test",
        )
        agent = TriageAgent(mock_classifier)
        
        result = agent.classify_ticket("I was charged twice")

        assert result.category == "billing_inquiry"
        assert result.confidence >= 0.70
        assert result.should_auto_respond() is False

    def test_classifies_feature_request(self):
        """RED: Test feature request classification"""
        mock_classifier = Mock()
        mock_classifier.classify.return_value = Mock(
            category="feature_request",
            priority=2,
            sentiment="positive",
            confidence=0.6,
            reasoning="Test",
        )
        agent = TriageAgent(mock_classifier)
        
        result = agent.classify_ticket("Would love dark mode")

        assert result.category == "feature_request"
        assert result.confidence >= 0.20
        assert result.should_auto_respond() is False

    def test_confidence_threshold_85_percent(self):
        """RED: Test that 85% confidence threshold determines auto-respond"""
        mock_classifier = Mock()
        mock_classifier.classify.return_value = Mock(
            category="password_reset",
            priority=3,
            sentiment="neutral",
            confidence=0.9,
            reasoning="Test",
        )
        agent = TriageAgent(mock_classifier)
        
        result = agent.classify_ticket("How do I reset?")

        # Should auto-respond when confidence > 85%
        if result.confidence > 0.85:
            assert result.should_auto_respond() is True
        else:
            assert result.should_auto_respond() is False

    def test_confidence_threshold_escalation(self):
        """RED: Test that low confidence triggers escalation"""
        mock_classifier = Mock()
        mock_classifier.classify.return_value = Mock(
            category="general_inquiry",
            priority=2,
            sentiment="neutral",
            confidence=0.5,
            reasoning="Test",
        )
        agent = TriageAgent(mock_classifier)
        
        result = agent.classify_ticket("Something isn't working")

        # Ambiguous tickets should have lower confidence
        assert result.confidence < 0.85
        assert result.should_auto_respond() is False
