# Hybrid response generator — templates first, RAG fallback

import logging
from typing import Optional

from agents.schema import TicketResponse

logger = logging.getLogger(__name__)


class HybridResponseGenerator:
    """Try keyword templates first; fall back to RAG when confidence is low.

    This saves API calls (and cost) for common, predictable tickets while
    providing grounded, KB-backed answers for complex ones.
    """

    def __init__(self, template_matcher, rag_generator):
        """
        Args:
            template_matcher:  TemplateMatcher instance.
            rag_generator:     LLMResponseGeneratorRAG instance.
        """
        self.matcher = template_matcher
        self.rag = rag_generator

        # Counters for cost analysis
        self.template_hits = 0
        self.rag_calls = 0

    def generate(self, ticket_text: str, category: str) -> TicketResponse:
        """Route ticket to template or RAG and return a TicketResponse."""
        # 1. Try fast template matching
        template_response = self.matcher.try_match(ticket_text)

        if template_response is not None:
            self.template_hits += 1
            logger.debug("Hybrid: template match — no API call")
            return TicketResponse(
                response_text=template_response,
                citations=["Template KB"],
                quality_score=0.75,
                needs_human_review=False,
            )

        # 2. Fall back to RAG
        self.rag_calls += 1
        logger.debug("Hybrid: no template match — calling RAG")
        return self.rag.generate(ticket_text, category)

    def cost_summary(self) -> dict:
        """Return a breakdown of template vs RAG usage."""
        total = self.template_hits + self.rag_calls
        template_rate = self.template_hits / total if total > 0 else 0.0
        return {
            "total_tickets": total,
            "template_hits": self.template_hits,
            "rag_calls": self.rag_calls,
            "template_deflection_rate": round(template_rate, 3),
        }
