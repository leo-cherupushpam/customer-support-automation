# Tests for TemplateMatcher

import pytest
from utils.template_matcher import TemplateMatcher


class TestTemplateMatcher:
    @pytest.fixture
    def matcher(self):
        return TemplateMatcher()

    # ------------------------------------------------------------------
    # 1. High-confidence match
    # ------------------------------------------------------------------
    def test_password_reset_match(self, matcher):
        """Password keywords produce a high-confidence password_reset match"""
        key, confidence = matcher.match(
            "I forgot my password and reset it — locked out and can't log in"
        )
        assert key == "password_reset"
        assert confidence >= 0.6

    def test_billing_match(self, matcher):
        """Billing keywords produce a billing_inquiry match"""
        key, confidence = matcher.match(
            "I have a charge on my billing invoice and need a payment receipt"
        )
        assert key == "billing_inquiry"
        assert confidence >= 0.5

    # ------------------------------------------------------------------
    # 2. No match
    # ------------------------------------------------------------------
    def test_no_match_returns_none(self, matcher):
        """Unrelated text returns (None, 0.0)"""
        key, confidence = matcher.match("I love this product it is amazing")
        assert key is None
        assert confidence == 0.0

    # ------------------------------------------------------------------
    # 3. try_match returns response above threshold
    # ------------------------------------------------------------------
    def test_try_match_returns_response_above_threshold(self, matcher):
        """try_match() returns a non-empty string when confidence >= threshold"""
        response = matcher.try_match(
            "I forgot my password, need to reset it, locked out and can't log in"
        )
        assert response is not None
        assert len(response) > 20

    def test_try_match_returns_none_below_threshold(self, matcher):
        """try_match() returns None for low-confidence / no match"""
        response = matcher.try_match("Hello there")
        assert response is None
