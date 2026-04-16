# Tests for OpenAI client

import pytest
from unittest.mock import Mock, patch
from services.openai_client import OpenAIClient


class TestOpenAIClient:
    def test_init_with_api_key(self):
        """Test initialization with API key"""
        with patch.dict("os.environ", {"OPENAI_API_KEY": "test_key"}):
            client = OpenAIClient()
            assert client.api_key == "test_key"
            assert client.model == "gpt-4o-mini"

    def test_init_without_api_key(self):
        """Test initialization fails without API key"""
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(ValueError, match="OPENAI_API_KEY"):
                OpenAIClient()

    def test_get_metrics(self):
        """Test metrics tracking"""
        with patch.dict("os.environ", {"OPENAI_API_KEY": "test_key"}):
            client = OpenAIClient()
            assert client.get_metrics() == {
                "total_calls": 0,
                "total_tokens": 0,
                "error_count": 0,
                "error_rate": 0.0,
            }
