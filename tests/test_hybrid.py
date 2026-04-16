# Tests for HybridResponseGenerator

import pytest
from unittest.mock import MagicMock
from agents.schema import TicketResponse


class TestHybridResponseGenerator:
    @pytest.fixture
    def mock_matcher_hit(self):
        """Template matcher that always returns a canned response"""
        m = MagicMock()
        m.try_match.return_value = "Step 1: Go to login. Step 2: Click Forgot Password."
        return m

    @pytest.fixture
    def mock_matcher_miss(self):
        """Template matcher that never matches"""
        m = MagicMock()
        m.try_match.return_value = None
        return m

    @pytest.fixture
    def mock_rag(self):
        """RAG generator stub"""
        rag = MagicMock()
        rag.generate.return_value = TicketResponse(
            response_text="Here is a RAG-generated answer.",
            citations=["Password Reset Guide"],
            quality_score=0.85,
            needs_human_review=False,
        )
        return rag

    @pytest.fixture
    def hybrid_hit(self, mock_matcher_hit, mock_rag):
        from agents.llm_response_generator_hybrid import HybridResponseGenerator

        return HybridResponseGenerator(mock_matcher_hit, mock_rag)

    @pytest.fixture
    def hybrid_miss(self, mock_matcher_miss, mock_rag):
        from agents.llm_response_generator_hybrid import HybridResponseGenerator

        return HybridResponseGenerator(mock_matcher_miss, mock_rag)

    # ------------------------------------------------------------------
    # 1. Template path
    # ------------------------------------------------------------------
    def test_template_hit_skips_rag(self, hybrid_hit, mock_rag):
        """When template matches, RAG is NOT called"""
        hybrid_hit.generate("I forgot my password", "password_reset")
        mock_rag.generate.assert_not_called()

    def test_template_hit_returns_ticket_response(self, hybrid_hit):
        """Template path returns a valid TicketResponse"""
        result = hybrid_hit.generate("I forgot my password", "password_reset")
        assert isinstance(result, TicketResponse)
        assert result.quality_score == 0.75

    # ------------------------------------------------------------------
    # 2. RAG fallback path
    # ------------------------------------------------------------------
    def test_rag_called_on_miss(self, hybrid_miss, mock_rag):
        """When template misses, RAG generate() is called"""
        hybrid_miss.generate("I need help with a complex issue", "general_inquiry")
        mock_rag.generate.assert_called_once()

    def test_rag_response_returned_on_miss(self, hybrid_miss):
        """RAG path returns the TicketResponse from the RAG generator"""
        result = hybrid_miss.generate("Complex issue", "general_inquiry")
        assert isinstance(result, TicketResponse)
        assert result.quality_score == 0.85

    # ------------------------------------------------------------------
    # 3. Cost summary
    # ------------------------------------------------------------------
    def test_cost_summary_tracks_correctly(self, mock_matcher_hit, mock_matcher_miss, mock_rag):
        from agents.llm_response_generator_hybrid import HybridResponseGenerator

        # Two template hits, one RAG call
        gen = HybridResponseGenerator(mock_matcher_hit, mock_rag)
        gen.generate("forgot password", "password_reset")
        gen.generate("reset password", "password_reset")

        # Swap to miss matcher for RAG call
        gen.matcher = mock_matcher_miss
        gen.generate("complex question", "general_inquiry")

        summary = gen.cost_summary()
        assert summary["template_hits"] == 2
        assert summary["rag_calls"] == 1
        assert summary["total_tickets"] == 3
        assert abs(summary["template_deflection_rate"] - 0.667) < 0.01
