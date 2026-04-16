# LLM-based response generator

import logging
from typing import Optional, List
from services.openai_client import OpenAIClient
from agents.schema import TicketResponse
from prompts.response_prompt import get_response_prompt

logger = logging.getLogger(__name__)


class LLMResponseGenerator:
    """LLM-based response generator with KB integration"""

    def __init__(self, openai_client: Optional[OpenAIClient] = None):
        self.client = openai_client or OpenAIClient()

    def generate(self, ticket_text: str, category: str, kb_articles: List[str] = None) -> TicketResponse:
        """Generate response using LLM"""
        try:
            messages = get_response_prompt(ticket_text, category, kb_articles)

            response = self.client.chat_completion(
                messages=messages,
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "ticket_response",
                        "schema": TicketResponse.model_json_schema(),
                    },
                },
            )

            # Parse response
            content = response.choices[0].message.content
            result = TicketResponse.model_validate_json(content)

            # Set human review flag based on quality
            result.needs_human_review = result.quality_score < 0.7

            return result

        except Exception as e:
            logger.error(f"LLM response generation failed: {e}")
            # Fallback: return default response
            return TicketResponse(
                response_text="Thank you for contacting us. A support agent will respond shortly.",
                citations=[],
                quality_score=0.5,
                needs_human_review=True,
            )

    def evaluate_quality(self, response_text: str) -> float:
        """Evaluate response quality (0.0-1.0)"""
        if not response_text or len(response_text) < 20:
            return 0.0

        # Simple heuristic for MVP
        length_score = min(1.0, len(response_text) / 200)
        helpful_phrases = ["thank", "please", "help", "happy"]
        phrase_score = sum(1 for phrase in helpful_phrases if phrase in response_text.lower()) * 0.05

        return min(1.0, length_score + phrase_score)

    def should_human_review(self, quality_score: float) -> bool:
        """Determine if response needs human review"""
        return quality_score < 0.7
