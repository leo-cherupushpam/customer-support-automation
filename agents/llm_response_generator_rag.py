# RAG-based response generator — wraps LLMResponseGenerator with context retrieval

import logging
from typing import List, Optional

from agents.llm_response_generator import LLMResponseGenerator
from agents.schema import TicketResponse

logger = logging.getLogger(__name__)


class LLMResponseGeneratorRAG(LLMResponseGenerator):
    """Response generator that injects RAG context before calling the LLM."""

    def __init__(self, rag_retriever, openai_client=None):
        """
        Args:
            rag_retriever:  RAGRetriever instance.
            openai_client:  Optional OpenAIClient (forwarded to parent).
        """
        super().__init__(openai_client=openai_client)
        self.rag = rag_retriever

    def generate(
        self,
        ticket_text: str,
        category: str,
        kb_articles: Optional[List[str]] = None,
    ) -> TicketResponse:
        """Retrieve relevant KB articles via RAG then generate a response.

        If ``kb_articles`` is already provided (e.g., cached), skip retrieval.
        """
        try:
            # Retrieve KB context when not pre-supplied
            if kb_articles is None:
                kb_articles = self.rag.retrieve(ticket_text, top_k=3)
                logger.debug(f"RAG retrieved {len(kb_articles)} articles for ticket")

            return super().generate(ticket_text, category, kb_articles)

        except Exception as e:
            logger.error(f"RAG response generation failed: {e}")
            return TicketResponse(
                response_text=(
                    "Thank you for contacting us. "
                    "A support agent will respond shortly."
                ),
                citations=[],
                quality_score=0.5,
                needs_human_review=True,
            )

    def answer_with_rag(self, ticket_text: str, category: str) -> str:
        """Convenience method: retrieve + generate, return plain text."""
        return self.rag.answer(ticket_text)
