# LLM-based ticket classifier

import logging
from typing import Optional, List
from services.openai_client import OpenAIClient
from agents.schema import TicketClassification
from prompts.classification_prompt import get_classification_prompt

logger = logging.getLogger(__name__)


class LLMClassifier:
    """LLM-based ticket classifier using GPT-4o-mini"""

    def __init__(self, openai_client: Optional[OpenAIClient] = None):
        self.client = openai_client or OpenAIClient()
        self.categories = [
            "password_reset",
            "billing_inquiry",
            "feature_request",
            "technical_issue",
            "general_inquiry",
        ]

    def classify(self, ticket_text: str) -> TicketClassification:
        """Classify a ticket using LLM"""
        try:
            messages = get_classification_prompt(ticket_text, self.categories)

            response = self.client.chat_completion(
                messages=messages,
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "ticket_classification",
                        "schema": TicketClassification.model_json_schema(),
                    },
                },
            )

            # Parse response
            content = response.choices[0].message.content
            return TicketClassification.model_validate_json(content)

        except Exception as e:
            logger.error(f"LLM classification failed: {e}")
            # Fallback: return default classification
            return TicketClassification(
                category="general_inquiry",
                priority=2,
                sentiment="neutral",
                confidence=0.5,
                reasoning=f"LLM error, defaulting: {str(e)}",
            )

    def classify_batch(self, tickets: List[str]) -> List[TicketClassification]:
        """Classify multiple tickets"""
        return [self.classify(ticket) for ticket in tickets]
