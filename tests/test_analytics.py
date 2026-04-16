# Tests for analytics tracking

import pytest
import tempfile
import os
import json
from utils.analytics import AnalyticsTracker


class TestAnalyticsTracker:
    """Test analytics tracking functionality"""

    def setup_method(self):
        """Create temporary file for each test"""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json')
        self.temp_file.close()

    def teardown_method(self):
        """Clean up temp file"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_track_ticket_processed(self):
        """Test tracking a processed ticket"""
        tracker = AnalyticsTracker(self.temp_file.name)
        
        tracker.track_ticket_processed(
            ticket_id="1",
            category="password_reset",
            auto_responded=True,
            confidence=0.9,
            tokens_used=100,
            response_time=0.5
        )
        
        stats = tracker.get_stats()
        assert stats["total_tickets"] == 1
        assert stats["auto_responded"] == 1
        assert stats["escalated"] == 0

    def test_track_escalated_ticket(self):
        """Test tracking an escalated ticket"""
        tracker = AnalyticsTracker(self.temp_file.name)
        
        tracker.track_ticket_processed(
            ticket_id="1",
            category="billing_inquiry",
            auto_responded=False,
            confidence=0.7,
            tokens_used=50,
            response_time=1.0
        )
        
        stats = tracker.get_stats()
        assert stats["total_tickets"] == 1
        assert stats["auto_responded"] == 0
        assert stats["escalated"] == 1

    def test_deflection_rate_calculation(self):
        """Test deflection rate calculation"""
        tracker = AnalyticsTracker(self.temp_file.name)
        
        # Track 10 tickets, 6 auto-responded
        for i in range(10):
            auto_responded = i < 6
            tracker.track_ticket_processed(
                ticket_id=str(i),
                category="general",
                auto_responded=auto_responded,
                confidence=0.8,
                tokens_used=100,
                response_time=0.5
            )
        
        stats = tracker.get_stats()
        assert stats["deflection_rate"] == 0.6  # 60%

    def test_token_usage_tracking(self):
        """Test token usage tracking"""
        tracker = AnalyticsTracker(self.temp_file.name)
        
        tracker.track_ticket_processed(
            ticket_id="1",
            category="password_reset",
            auto_responded=True,
            confidence=0.9,
            tokens_used=150,
            response_time=0.5
        )
        
        stats = tracker.get_stats()
        assert stats["total_tokens"] == 150

    def test_cost_estimation(self):
        """Test cost estimation based on tokens"""
        tracker = AnalyticsTracker(self.temp_file.name)
        
        # 1000 tickets × 200 tokens each = 200,000 tokens
        for i in range(1000):
            tracker.track_ticket_processed(
                ticket_id=str(i),
                category="general",
                auto_responded=True,
                confidence=0.8,
                tokens_used=200,
                response_time=0.5
            )
        
        stats = tracker.get_stats()
        # GPT-4o-mini: $0.15/M input, $0.60/M output
        # Cost = tokens * rate_per_token (0.00018 per token for combined input+output)
        # 200,000 tokens * $0.00018 / 1,000,000 = $0.036
        expected_cost = 200000 * 0.00018 / 1000000
        assert abs(stats["estimated_cost"] - expected_cost) < 0.001

    def test_average_response_time(self):
        """Test average response time calculation"""
        tracker = AnalyticsTracker(self.temp_file.name)
        
        tracker.track_ticket_processed(
            ticket_id="1",
            category="general",
            auto_responded=True,
            confidence=0.8,
            tokens_used=100,
            response_time=0.5
        )
        tracker.track_ticket_processed(
            ticket_id="2",
            category="general",
            auto_responded=True,
            confidence=0.8,
            tokens_used=100,
            response_time=1.5
        )
        
        stats = tracker.get_stats()
        assert stats["average_response_time"] == 1.0  # (0.5 + 1.5) / 2

    def test_category_distribution(self):
        """Test category distribution tracking"""
        tracker = AnalyticsTracker(self.temp_file.name)
        
        # Track tickets with different categories
        tracker.track_ticket_processed(
            ticket_id="1",
            category="password_reset",
            auto_responded=True,
            confidence=0.9,
            tokens_used=100,
            response_time=0.5
        )
        tracker.track_ticket_processed(
            ticket_id="2",
            category="password_reset",
            auto_responded=True,
            confidence=0.9,
            tokens_used=100,
            response_time=0.5
        )
        tracker.track_ticket_processed(
            ticket_id="3",
            category="billing_inquiry",
            auto_responded=False,
            confidence=0.7,
            tokens_used=100,
            response_time=0.5
        )
        
        stats = tracker.get_stats()
        assert stats["category_distribution"]["password_reset"] == 2
        assert stats["category_distribution"]["billing_inquiry"] == 1

    def test_persistence(self):
        """Test that analytics are persisted to file"""
        tracker = AnalyticsTracker(self.temp_file.name)
        
        tracker.track_ticket_processed(
            ticket_id="1",
            category="general",
            auto_responded=True,
            confidence=0.8,
            tokens_used=100,
            response_time=0.5
        )
        
        # Create new tracker from same file
        tracker2 = AnalyticsTracker(self.temp_file.name)
        stats = tracker2.get_stats()
        
        assert stats["total_tickets"] == 1

    def test_reset_stats(self):
        """Test resetting statistics"""
        tracker = AnalyticsTracker(self.temp_file.name)
        
        tracker.track_ticket_processed(
            ticket_id="1",
            category="general",
            auto_responded=True,
            confidence=0.8,
            tokens_used=100,
            response_time=0.5
        )
        
        tracker.reset_stats()
        
        stats = tracker.get_stats()
        assert stats["total_tickets"] == 0
        assert stats["auto_responded"] == 0
