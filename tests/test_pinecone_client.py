# Tests for PineconeClient

import pytest
from unittest.mock import MagicMock, patch, PropertyMock


class TestPineconeClient:
    @pytest.fixture
    def mock_pinecone_module(self):
        """Patch the pinecone module so no real connection is made"""
        with patch.dict("sys.modules", {"pinecone": MagicMock()}):
            import importlib
            import utils.pinecone_client as pc_module
            importlib.reload(pc_module)
            yield pc_module

    @pytest.fixture
    def client(self):
        """Build a PineconeClient with a fully mocked Pinecone backend"""
        from utils.pinecone_client import PineconeClient

        with patch("utils.pinecone_client.PineconeClient._get_client"):
            c = PineconeClient(api_key="test_key")
            # Inject a mock index directly
            mock_index = MagicMock()
            c._index = mock_index
            c._client = MagicMock()
            return c

    # ------------------------------------------------------------------
    # 1. Initialization
    # ------------------------------------------------------------------
    def test_client_initialization_with_key(self):
        """Constructor stores provided API key"""
        from utils.pinecone_client import PineconeClient

        with patch("utils.pinecone_client.PineconeClient._get_client"):
            c = PineconeClient(api_key="test_key_123")
            assert c.api_key == "test_key_123"
            assert c.INDEX_NAME == "customer-support-kb"

    def test_client_raises_without_api_key(self, monkeypatch):
        """Constructor raises ValueError when no API key available"""
        monkeypatch.delenv("PINECONE_API_KEY", raising=False)

        from utils.pinecone_client import PineconeClient

        with pytest.raises(ValueError, match="PINECONE_API_KEY"):
            PineconeClient()

    # ------------------------------------------------------------------
    # 2. Upsert
    # ------------------------------------------------------------------
    def test_upsert_calls_index(self, client):
        """upsert() forwards vectors to the Pinecone index"""
        vectors = [
            {"id": "1", "values": [0.1] * 1536, "metadata": {"text": "hello"}},
            {"id": "2", "values": [0.2] * 1536, "metadata": {"text": "world"}},
        ]
        count = client.upsert(vectors)

        client._index.upsert.assert_called_once_with(vectors=vectors)
        assert count == 2

    # ------------------------------------------------------------------
    # 3. Query
    # ------------------------------------------------------------------
    def test_query_returns_matches(self, client):
        """query() returns matches from Pinecone response"""
        fake_match = MagicMock()
        fake_match.metadata = {"content": "Reset your password at settings."}
        client._index.query.return_value = MagicMock(matches=[fake_match, fake_match])

        results = client.query([0.1] * 1536, top_k=2)

        client._index.query.assert_called_once()
        assert len(results) == 2

    def test_query_top_k_respected(self, client):
        """query() passes top_k to index"""
        client._index.query.return_value = MagicMock(matches=[])

        client.query([0.0] * 1536, top_k=5)

        call_kwargs = client._index.query.call_args[1]
        assert call_kwargs["top_k"] == 5

    # ------------------------------------------------------------------
    # 4. Delete all
    # ------------------------------------------------------------------
    def test_delete_all(self, client):
        """delete_all() calls index delete with delete_all=True"""
        client.delete_all()
        client._index.delete.assert_called_once_with(delete_all=True)
