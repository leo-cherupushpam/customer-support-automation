# Tests for priority routing

import pytest
from src.agents.escalation_agent import EscalationAgent, EscalationTicket


class TestPriorityRouting:
    """Test priority routing functionality"""

    def setup_method(self):
        """Initialize Escalation Agent"""
        self.agent = EscalationAgent()

    def test_urgent_ticket_high_priority(self):
        """Test that urgent tickets get high priority"""
        escalation = self.agent.create_escalation(
            ticket_text="URGENT: My account is locked and I can't access it!",
            category="technical_issue",
            confidence=0.6
        )
        
        assert escalation.priority in ['high', 'urgent']

    def test_refund_request_high_priority(self):
        """Test that refund requests get high priority"""
        escalation = self.agent.create_escalation(
            ticket_text="I need an immediate refund, this is unacceptable!",
            category="billing_inquiry",
            confidence=0.7
        )
        
        assert escalation.priority in ['high', 'urgent']

    def test_feature_request_low_priority(self):
        """Test that feature requests get low priority"""
        escalation = self.agent.create_escalation(
            ticket_text="Would love to see dark mode in the app",
            category="feature_request",
            confidence=0.8
        )
        
        assert escalation.priority == 'low'

    def test_general_inquiry_medium_priority(self):
        """Test that general inquiries get medium priority"""
        escalation = self.agent.create_escalation(
            ticket_text="What are your business hours?",
            category="general_inquiry",
            confidence=0.75
        )
        
        assert escalation.priority == 'medium'

    def test_low_confidence_high_priority(self):
        """Test that low confidence tickets get higher priority"""
        escalation = self.agent.create_escalation(
            ticket_text="Something isn't working right",
            category="general_inquiry",
            confidence=0.4
        )
        
        assert escalation.priority in ['high', 'urgent']

    def test_negative_sentiment_higher_priority(self):
        """Test that negative sentiment increases priority"""
        escalation = self.agent.create_escalation(
            ticket_text="This is the third time this has happened! I want a refund!",
            category="billing_inquiry",
            confidence=0.8
        )
        
        assert escalation.priority in ['high', 'urgent']

    def test_context_summary_includes_priority(self):
        """Test that context summary includes priority information"""
        escalation = self.agent.create_escalation(
            ticket_text="URGENT: Payment failed",
            category="billing_inquiry",
            confidence=0.6
        )
        
        assert "priority" in escalation.context_summary.lower()
        assert escalation.priority.upper() in escalation.context_summary
