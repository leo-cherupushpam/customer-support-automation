# Tests for prompts

import pytest
from prompts.classification_prompt import get_classification_prompt
from prompts.response_prompt import get_response_prompt


class TestClassificationPrompts:
    def test_classification_prompt_structure(self):
        """Test classification prompt has correct structure"""
        prompt = get_classification_prompt("I forgot my password")

        assert len(prompt) == 2
        assert prompt[0]["role"] == "system"
        assert prompt[1]["role"] == "user"
        assert "password" in prompt[1]["content"].lower()

    def test_classification_prompt_categories(self):
        """Test classification prompt includes categories"""
        prompt = get_classification_prompt("Test ticket")

        assert "password_reset" in prompt[0]["content"]
        assert "billing_inquiry" in prompt[0]["content"]


class TestResponsePrompts:
    def test_response_prompt_structure(self):
        """Test response prompt has correct structure"""
        prompt = get_response_prompt("Test", "password_reset")

        assert len(prompt) == 2
        assert prompt[0]["role"] == "system"
        assert prompt[1]["role"] == "user"

    def test_response_prompt_includes_category(self):
        """Test response prompt includes category"""
        prompt = get_response_prompt("Test", "billing_inquiry")

        assert "billing_inquiry" in prompt[1]["content"]
