# Tests for LLMResponseGeneratorRAG

import pytest
from unittest.mock import MagicMock, patch
from agents.schema import TicketResponse


class TestLLMResponseGeneratorRAG:
    @pytest.fixture
    def mock_openai(self):
        client = MagicMock()
        client.chat_completion.return_value = MagicMock(
            choices=[
                MagicMock(
                    message=MagicMock(
                        content=(
                            '{"response_text": "Here is how to reset your password: ...", '
                            '"citations": ["Password Reset Guide"], '
                            '"quality_score": 0.9, "needs_human_review": false}'
                        )
                    )
                )
            ]
        )
        return client

    @pytest.fixture
    def mock_rag(self):
        rag = MagicMock()
        rag.retrieve.return_value = ["Article: Password Reset Guide\n\nStep 1: ..."]
        rag.answer.return_value = "Here is how to reset your password."
        return rag

    @pytest.fixture
    def generator(self, mock_rag, mock_openai):
        from agents.llm_response_generator_rag import LLMResponseGeneratorRAG

        return LLMResponseGeneratorRAG(rag_retriever=mock_rag, openai_client=mock_openai)

    # ------------------------------------------------------------------
    # 1. RAG retrieval is called when no kb_articles provided
    # ------------------------------------------------------------------
    def test_generate_calls_rag_retrieve(self, generator, mock_rag):
        """generate() retrieves context via RAG when kb_articles is None"""
        generator.generate("I forgot my password", "password_reset")
        mock_rag.retrieve.assert_called_once_with("I forgot my password", top_k=3)

    # ------------------------------------------------------------------
    # 2. Pre-supplied kb_articles skip retrieval
    # ------------------------------------------------------------------
    def test_generate_skips_rag_when_articles_provided(self, generator, mock_rag):
        """generate() does NOT call RAG when kb_articles is already given"""
        generator.generate(
            "I forgot my password",
            "password_reset",
            kb_articles=["KB: pre-fetched article"],
        )
        mock_rag.retrieve.assert_not_called()

    # ------------------------------------------------------------------
    # 3. Returns TicketResponse
    # ------------------------------------------------------------------
    def test_generate_returns_ticket_response(self, generator):
        """generate() returns a TicketResponse instance"""
        result = generator.generate("I forgot my password", "password_reset")
        assert isinstance(result, TicketResponse)
        assert len(result.response_text) > 0

    # ------------------------------------------------------------------
    # 4. Fallback on error
    # ------------------------------------------------------------------
    def test_generate_fallback_on_rag_error(self, mock_openai):
        """generate() returns fallback TicketResponse when RAG raises"""
        from agents.llm_response_generator_rag import LLMResponseGeneratorRAG

        broken_rag = MagicMock()
        broken_rag.retrieve.side_effect = Exception("Pinecone unreachable")

        gen = LLMResponseGeneratorRAG(rag_retriever=broken_rag, openai_client=mock_openai)
        result = gen.generate("test", "general_inquiry")

        assert result.needs_human_review is True
        assert result.quality_score == 0.5

    # ------------------------------------------------------------------
    # 5. answer_with_rag convenience method
    # ------------------------------------------------------------------
    def test_answer_with_rag_returns_string(self, generator, mock_rag):
        """answer_with_rag() returns a plain string"""
        result = generator.answer_with_rag("How do I reset my password?", "password_reset")
        assert isinstance(result, str)
        mock_rag.answer.assert_called_once_with("How do I reset my password?")
