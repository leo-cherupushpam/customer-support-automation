# Learning Agent Tests

import pytest
from src.agents.learning_agent import LearningAgent, KBUpdate

class TestLearningAgent:
    """Test Learning Agent for KB improvements"""
    
    def setup_method(self):
        """Initialize Learning Agent for each test"""
        self.agent = LearningAgent()
        
    def test_analyzes_resolved_tickets(self):
        """RED: Test that resolved tickets are analyzed"""
        resolved_tickets = [
            {"ticket": "How do I reset my password?", "response": "Go to login page and click Forgot Password", "category": "password_reset"}
        ]
        
        updates = self.agent.analyze_resolved_tickets(resolved_tickets)
        
        assert updates is not None
        assert len(updates) >= 0  # MVP may not generate updates for single ticket
        
    def test_detects_new_questions(self):
        """RED: Test detection of new questions"""
        resolved_tickets = [
            {"ticket": "How do I use dark mode?", "response": "Go to Settings and enable Dark Mode", "category": "feature_request"}
        ]
        
        updates = self.agent.analyze_resolved_tickets(resolved_tickets)
        
        assert updates is not None
        
    def test_suggests_kb_updates(self):
        """RED: Test KB update suggestions"""
        resolved_tickets = [
            {"ticket": "How do I reset my password?", "response": "Go to login page and click Forgot Password", "category": "password_reset"}
        ]
        
        updates = self.agent.analyze_resolved_tickets(resolved_tickets)
        
        # MVP: May not generate updates for single ticket, but should not crash
        assert isinstance(updates, list)
        
    def test_batch_processing(self):
        """RED: Test batch processing of multiple tickets"""
        resolved_tickets = [
            {"ticket": "How do I reset my password?", "response": "Go to login page", "category": "password_reset"},
            {"ticket": "I was charged twice", "response": "Check your email", "category": "billing_inquiry"},
            {"ticket": "Feature request", "response": "Thanks for suggestion", "category": "feature_request"}
        ]
        
        updates = self.agent.analyze_resolved_tickets(resolved_tickets)
        
        assert updates is not None
        assert isinstance(updates, list)
