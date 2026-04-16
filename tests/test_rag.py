# Tests for RAGRetriever

import pytest
from unittest.mock import MagicMock, call


class TestRAGRetriever:
    @pytest.fixture
    def mock_openai(self):
        client = MagicMock()
        # embeddings stub
        emb_resp = MagicMock()
        emb_resp.data = [MagicMock(embedding=[0.1] * 1536)]
        client.embeddings.create.return_value = emb_resp
        # chat completion stub
        chat_resp = MagicMock()
        chat_resp.choices = [MagicMock(message=MagicMock(content="Here is your answer."))]
        client.chat_completion.return_value = chat_resp
        return client

    @pytest.fixture
    def mock_pinecone(self):
        client = MagicMock()
        match = MagicMock()
        match.metadata = {"content": "Reset your password at settings.", "title": "Password Reset Guide"}
        client.query.return_value = [match, match]
        return client

    @pytest.fixture
    def retriever(self, mock_openai, mock_pinecone):
        from utils.rag import RAGRetriever

        return RAGRetriever(pinecone_client=mock_pinecone, openai_client=mock_openai)

    # ------------------------------------------------------------------
    # 1. Embedding
    # ------------------------------------------------------------------
    def test_embed_query_calls_openai(self, retriever, mock_openai):
        """_embed_query calls OpenAI embeddings with correct model"""
        retriever._embed_query("reset my password")
        mock_openai.embeddings.create.assert_called_once_with(
            input="reset my password",
            model="text-embedding-ada-002",
        )

    # ------------------------------------------------------------------
    # 2. Retrieval
    # ------------------------------------------------------------------
    def test_retrieve_returns_content_list(self, retriever, mock_pinecone):
        """retrieve() returns a list of content strings"""
        results = retriever.retrieve("reset my password", top_k=2)
        assert isinstance(results, list)
        assert all(isinstance(r, str) for r in results)

    def test_retrieve_passes_top_k(self, retriever, mock_pinecone):
        """retrieve() passes top_k to Pinecone"""
        retriever.retrieve("billing issue", top_k=5)
        call_kwargs = mock_pinecone.query.call_args[1]
        assert call_kwargs["top_k"] == 5

    # ------------------------------------------------------------------
    # 3. Generation
    # ------------------------------------------------------------------
    def test_generate_response_with_context(self, retriever, mock_openai):
        """generate_response() calls chat_completion when context is provided"""
        context = ["Article content 1", "Article content 2"]
        response = retriever.generate_response("How do I reset my password?", context)
        mock_openai.chat_completion.assert_called_once()
        assert isinstance(response, str)
        assert len(response) > 0

    def test_generate_response_empty_context(self, retriever, mock_openai):
        """generate_response() returns fallback message when context is empty"""
        response = retriever.generate_response("How do I reset my password?", [])
        mock_openai.chat_completion.assert_not_called()
        assert "knowledge base" in response.lower() or "support agent" in response.lower()

    # ------------------------------------------------------------------
    # 4. End-to-end
    # ------------------------------------------------------------------
    def test_answer_end_to_end(self, retriever):
        """answer() retrieves context then generates a response"""
        result = retriever.answer("I forgot my password")
        assert isinstance(result, str)
        assert len(result) > 0
