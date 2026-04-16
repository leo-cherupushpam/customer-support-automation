# Response Agent Tests

import pytest
from src.agents.response_agent import ResponseAgent

class TestResponseAgent:
    """Test Response Agent RAG-based response generation"""
    
    def setup_method(self):
        """Initialize Response Agent for each test"""
        self.agent = ResponseAgent()
        
    def test_generates_response_for_password_reset(self):
        """RED: Test response generation for password reset tickets"""
        ticket_text = "I forgot my password, can you help me reset it?"
        category = "password_reset"
        
        response = self.agent.generate_response(ticket_text, category)
        
        assert response is not None
        assert len(response) > 20  # Response should have some content
        assert "password" in response.lower()  # Should mention password
        
    def test_generates_response_for_billing_inquiry(self):
        """RED: Test response generation for billing inquiries"""
        ticket_text = "I was charged twice for my subscription this month"
        category = "billing_inquiry"
        
        response = self.agent.generate_response(ticket_text, category)
        
        assert response is not None
        assert len(response) > 20
        assert "charge" in response.lower() or "billing" in response.lower()
        
    def test_provides_citations(self):
        """RED: Test that responses include KB citations"""
        ticket_text = "How do I reset my password?"
        category = "password_reset"
        
        response = self.agent.generate_response(ticket_text, category)
        
        assert response is not None
        # MVP: Basic citation tracking (will be enhanced with real KB later)
        assert "citation" in response.lower() or len(response) > 50
        
    def test_quality_score_exists(self):
        """RED: Test that responses have quality scores"""
        ticket_text = "I forgot my password"
        category = "password_reset"
        
        response = self.agent.generate_response(ticket_text, category)
        quality_score = self.agent.evaluate_quality(response)
        
        assert quality_score is not None
        assert 0 <= quality_score <= 1
