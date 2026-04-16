# Escalation Agent Tests

import pytest
from src.agents.escalation_agent import EscalationAgent, EscalationTicket

class TestEscalationAgent:
    """Test Escalation Agent for human handoff"""
    
    def setup_method(self):
        """Initialize Escalation Agent for each test"""
        self.agent = EscalationAgent()
        
    def test_creates_escalation_ticket(self):
        """RED: Test that low-confidence tickets create escalation tickets"""
        ticket_text = "I'm not sure what my issue is, but something is wrong"
        category = "general_inquiry"
        confidence = 0.65
        
        escalation = self.agent.create_escalation(ticket_text, category, confidence)
        
        assert escalation is not None
        assert escalation.context_summary is not None
        assert len(escalation.context_summary) > 20
        
    def test_generates_context_summary(self):
        """RED: Test context summary generation"""
        ticket_text = "I was charged twice and need a refund urgently"
        category = "billing_inquiry"
        confidence = 0.70
        
        escalation = self.agent.create_escalation(ticket_text, category, confidence)
        
        assert escalation.context_summary is not None
        assert len(escalation.context_summary) > 30
        assert "charged" in escalation.context_summary.lower() or "billing" in escalation.context_summary.lower()
        
    def test_drafts_suggested_response(self):
        """RED: Test suggested response draft"""
        ticket_text = "How do I reset my password?"
        category = "password_reset"
        confidence = 0.80
        
        escalation = self.agent.create_escalation(ticket_text, category, confidence)
        
        assert escalation.suggested_response is not None
        assert len(escalation.suggested_response) > 20
        
    def test_assigns_priority(self):
        """RED: Test priority assignment"""
        ticket_text = "URGENT: My account is locked and I can't access it!"
        category = "technical_issue"
        confidence = 0.60
        
        escalation = self.agent.create_escalation(ticket_text, category, confidence)
        
        assert escalation.priority is not None
        assert escalation.priority in ['low', 'medium', 'high', 'urgent']
        
    def test_urgent_tickets_get_high_priority(self):
        """RED: Test that urgent keywords increase priority"""
        ticket_text = "URGENT: My account is locked!"
        category = "technical_issue"
        confidence = 0.55
        
        escalation = self.agent.create_escalation(ticket_text, category, confidence)
        
        assert escalation.priority in ['high', 'urgent']
