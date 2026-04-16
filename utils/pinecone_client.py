# Pinecone vector database client

import logging
import os
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class PineconeClient:
    """Pinecone vector database client for KB retrieval"""

    INDEX_NAME = "customer-support-kb"
    DIMENSION = 1536  # text-embedding-ada-002

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("PINECONE_API_KEY")
        if not self.api_key:
            raise ValueError("PINECONE_API_KEY not found in environment")

        self._client = None
        self._index = None

    def _get_client(self):
        """Lazy-initialize Pinecone client"""
        if self._client is None:
            from pinecone import Pinecone, ServerlessSpec  # noqa: PLC0415

            self._client = Pinecone(api_key=self.api_key)
            self._ensure_index()
        return self._client

    def _ensure_index(self):
        """Create index if it does not exist"""
        from pinecone import ServerlessSpec  # noqa: PLC0415

        existing = [i.name for i in self._client.list_indexes()]
        if self.INDEX_NAME not in existing:
            logger.info(f"Creating Pinecone index: {self.INDEX_NAME}")
            self._client.create_index(
                name=self.INDEX_NAME,
                dimension=self.DIMENSION,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )
        self._index = self._client.Index(self.INDEX_NAME)

    @property
    def index(self):
        """Return the active index, initializing if needed"""
        self._get_client()
        return self._index

    def upsert(self, vectors: List[Dict]) -> int:
        """Upsert vectors to index. Returns count upserted."""
        self.index.upsert(vectors=vectors)
        return len(vectors)

    def query(self, query_vector: List[float], top_k: int = 3) -> List[Dict]:
        """Query index for similar vectors. Returns list of matches with metadata."""
        response = self.index.query(
            vector=query_vector,
            top_k=top_k,
            include_metadata=True,
        )
        return list(response.matches)

    def delete_all(self):
        """Delete all vectors from index (useful for testing/reset)."""
        self.index.delete(delete_all=True)

    def describe_index_stats(self) -> Dict:
        """Return index statistics."""
        return self.index.describe_index_stats()
