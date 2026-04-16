# Triage Agent Tests

import pytest
from src.agents.triage_agent import TriageAgent, ClassificationResult

class TestTriageAgent:
    """Test Triage Agent classification and confidence scoring"""
    
    def setup_method(self):
        """Initialize Triage Agent for each test"""
        self.agent = TriageAgent()
        
    def test_classifies_password_reset_ticket(self):
        """RED: Test that password reset tickets are classified correctly"""
        ticket_text = "I forgot my password, can you help me reset it?"
        
        # This should fail initially (no implementation)
        result = self.agent.classify_ticket(ticket_text)
        
        assert result.category == "password_reset"
        assert result.confidence >= 0.85
        assert result.should_auto_respond() is True
        
    def test_classifies_billing_inquiry(self):
        """RED: Test billing inquiry classification"""
        ticket_text = "I was charged twice for my subscription this month"
        
        result = self.agent.classify_ticket(ticket_text)
        
        assert result.category == "billing_inquiry"
        assert result.confidence >= 0.70  # MVP can handle 70%+ for billing
        # Billing inquiries with 70-85% confidence still need human review
        assert result.should_auto_respond() is False
        
    def test_classifies_feature_request(self):
        """RED: Test feature request classification"""
        ticket_text = "Would love to see dark mode in the mobile app"
        
        result = self.agent.classify_ticket(ticket_text)
        
        assert result.category == "feature_request"
        assert result.confidence >= 0.20  # Feature requests get lower confidence
        assert result.should_auto_respond() is False  # Feature requests need human review
        
    def test_confidence_threshold_85_percent(self):
        """RED: Test that 85% confidence threshold determines auto-respond"""
        ticket_text = "How do I reset my password?"
        
        result = self.agent.classify_ticket(ticket_text)
        
        # Should auto-respond when confidence > 85%
        if result.confidence > 0.85:
            assert result.should_auto_respond() is True
        else:
            assert result.should_auto_respond() is False
            
    def test_confidence_threshold_escalation(self):
        """RED: Test that low confidence triggers escalation"""
        ticket_text = "I'm not sure what my issue is, but something is wrong"
        
        result = self.agent.classify_ticket(ticket_text)
        
        # Ambiguous tickets should have lower confidence
        assert result.confidence < 0.85
        assert result.should_auto_respond() is False
