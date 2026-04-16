# Tests for KBEmbedder

import os
import pytest
from unittest.mock import MagicMock, patch


ARTICLES_FILE = os.path.join(
    os.path.dirname(__file__), "..", "knowledge_base", "articles.md"
)


class TestKBEmbedder:
    @pytest.fixture
    def mock_openai(self):
        """OpenAI client stub that returns a fixed-length embedding"""
        client = MagicMock()
        embedding_obj = MagicMock()
        embedding_obj.data = [MagicMock(embedding=[0.1] * 1536)]
        client.embeddings.create.return_value = embedding_obj
        return client

    @pytest.fixture
    def mock_pinecone(self):
        """PineconeClient stub"""
        return MagicMock()

    @pytest.fixture
    def embedder(self, mock_openai, mock_pinecone):
        from knowledge_base.create_embeddings import KBEmbedder

        return KBEmbedder(openai_client=mock_openai, pinecone_client=mock_pinecone)

    # ------------------------------------------------------------------
    # 1. Article extraction
    # ------------------------------------------------------------------
    def test_extract_articles_count(self, embedder):
        """Extracts exactly 15 articles from the KB file"""
        articles = embedder.extract_articles(ARTICLES_FILE)
        assert len(articles) == 15

    def test_extract_articles_have_required_keys(self, embedder):
        """Each article has id, title, and content keys"""
        articles = embedder.extract_articles(ARTICLES_FILE)
        for article in articles:
            assert "id" in article
            assert "title" in article
            assert "content" in article

    def test_extract_articles_no_empty_content(self, embedder):
        """No article has blank content"""
        articles = embedder.extract_articles(ARTICLES_FILE)
        for article in articles:
            assert len(article["content"]) > 50, f"Short content in: {article['title']}"

    # ------------------------------------------------------------------
    # 2. Embedding + upsert
    # ------------------------------------------------------------------
    def test_create_and_store_embeddings_returns_count(self, embedder, mock_pinecone):
        """Returns the number of articles upserted"""
        count = embedder.create_and_store_embeddings(ARTICLES_FILE)
        assert count == 15

    def test_create_and_store_embeddings_calls_upsert(self, embedder, mock_pinecone):
        """Calls pinecone.upsert once with a list of 15 vectors"""
        embedder.create_and_store_embeddings(ARTICLES_FILE)
        mock_pinecone.upsert.assert_called_once()
        vectors_arg = mock_pinecone.upsert.call_args[0][0]
        assert len(vectors_arg) == 15

    def test_vectors_have_correct_structure(self, embedder, mock_pinecone):
        """Each upserted vector has id, values (length 1536), and metadata"""
        embedder.create_and_store_embeddings(ARTICLES_FILE)
        vectors = mock_pinecone.upsert.call_args[0][0]
        for v in vectors:
            assert "id" in v
            assert len(v["values"]) == 1536
            assert "title" in v["metadata"]
            assert "content" in v["metadata"]
