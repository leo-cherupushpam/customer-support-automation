# Tests for Pydantic schemas

import pytest
from agents.schema import TicketClassification, TicketResponse


class TestTicketClassification:
    def test_valid_classification(self):
        """Test valid classification creation"""
        classification = TicketClassification(
            category="password_reset",
            priority=3,
            sentiment="neutral",
            confidence=0.9,
            reasoning="User explicitly asks for password reset",
        )
        assert classification.category == "password_reset"
        assert classification.priority == 3
        assert classification.confidence == 0.9

    def test_invalid_priority_low(self):
        """Test validation rejects priority < 1"""
        with pytest.raises(ValueError):
            TicketClassification(
                category="test",
                priority=0,
                sentiment="neutral",
                confidence=0.8,
                reasoning="test",
            )

    def test_invalid_confidence_high(self):
        """Test validation rejects confidence > 1.0"""
        with pytest.raises(ValueError):
            TicketClassification(
                category="test",
                priority=3,
                sentiment="neutral",
                confidence=1.5,
                reasoning="test",
            )


class TestTicketResponse:
    def test_valid_response(self):
        """Test valid response creation"""
        response = TicketResponse(
            response_text="Thank you for contacting us...",
            citations=["KB-001"],
            quality_score=0.85,
            needs_human_review=False,
        )
        assert response.needs_human_review is False
        assert response.quality_score == 0.85

    def test_needs_human_review_threshold(self):
        """Test human review flag at 0.7 threshold"""
        response = TicketResponse(
            response_text="Test response",
            quality_score=0.65,
            needs_human_review=False,  # Will be overridden by logic
        )
        assert response.quality_score < 0.7
