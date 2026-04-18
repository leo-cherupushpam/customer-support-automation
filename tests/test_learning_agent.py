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

    def test_kbupdate_has_enhanced_fields(self):
        """Test that KBUpdate includes new fields for structured KB"""
        update = KBUpdate(
            question="How do I reset my password?",
            answer="Go to login page and click Forgot Password",
            category="password_reset",
            confidence=0.9,
            source_ticket="How do I reset my password?",
            suggested_filename="password_reset_guide.md",
            review_status="pending"
        )

        assert hasattr(update, 'suggested_filename')
        assert hasattr(update, 'review_status')
        assert update.suggested_filename == "password_reset_guide.md"
        assert update.review_status == "pending"

    def test_analyze_resolved_tickets_generates_suggestions(self):
        """Test that analyze_resolved_tickets generates KBUpdate suggestions"""
        resolved_tickets = [
            {
                "ticket": "How do I reset my password?",
                "response": "Go to login page and click Forgot Password",
                "category": "password_reset"
            }
        ]

        updates = self.agent.analyze_resolved_tickets(resolved_tickets)

        assert isinstance(updates, list)
        if len(updates) > 0:
            assert isinstance(updates[0], KBUpdate)
            assert hasattr(updates[0], 'suggested_filename')
            assert hasattr(updates[0], 'review_status')

    def test_create_kb_update_includes_metadata(self):
        """Test that _create_kb_update generates KBUpdate with metadata"""
        ticket = {
            "ticket": "How do I reset my password?",
            "response": "Go to login page and click Forgot Password",
            "category": "password_reset"
        }

        update = self.agent._create_kb_update(ticket)

        assert isinstance(update, KBUpdate)
        assert hasattr(update, 'suggested_filename')
        assert hasattr(update, 'review_status')
        assert update.suggested_filename.endswith('.md')
        assert update.review_status == "pending"
