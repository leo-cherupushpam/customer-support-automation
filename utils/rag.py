# RAG-based retrieval and generation utility

import logging
from typing import List

logger = logging.getLogger(__name__)

_RAG_PROMPT_TEMPLATE = """You are a helpful customer support agent.
Use ONLY the context below to answer the customer's question.
If the context does not contain enough information, say so and offer to escalate.

Context:
{context}

Customer Question: {query}

Provide a clear, concise response. Cite the relevant article title(s) in brackets, e.g. [Password Reset Guide].
"""


class RAGRetriever:
    """Retrieve KB articles and generate grounded responses."""

    def __init__(self, pinecone_client, openai_client):
        """
        Args:
            pinecone_client: PineconeClient instance.
            openai_client:   OpenAIClient instance (chat_completion + embeddings).
        """
        self.pinecone = pinecone_client
        self.openai = openai_client

    # ------------------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------------------

    def _embed_query(self, query: str) -> List[float]:
        """Create a query embedding using text-embedding-ada-002."""
        response = self.openai.embeddings.create(
            input=query,
            model="text-embedding-ada-002",
        )
        return response.data[0].embedding

    def retrieve(self, query: str, top_k: int = 3) -> List[str]:
        """Return the top-k KB article contents most relevant to *query*."""
        query_vector = self._embed_query(query)
        matches = self.pinecone.query(query_vector=query_vector, top_k=top_k)
        return [m.metadata["content"] for m in matches if hasattr(m, "metadata")]

    # ------------------------------------------------------------------
    # Generation
    # ------------------------------------------------------------------

    def generate_response(self, query: str, context: List[str]) -> str:
        """Generate a grounded response from retrieved context."""
        if not context:
            return (
                "I'm sorry, I couldn't find relevant information in our knowledge base. "
                "A support agent will follow up with you shortly."
            )

        context_text = "\n\n---\n\n".join(context)
        prompt = _RAG_PROMPT_TEMPLATE.format(context=context_text, query=query)

        response = self.openai.chat_completion(
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content

    # ------------------------------------------------------------------
    # Convenience: retrieve + generate in one call
    # ------------------------------------------------------------------

    def answer(self, query: str, top_k: int = 3) -> str:
        """End-to-end: retrieve context and generate a response."""
        context = self.retrieve(query, top_k=top_k)
        return self.generate_response(query, context)
