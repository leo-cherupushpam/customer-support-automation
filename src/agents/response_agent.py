# Response Agent - LLM-based response generation

from typing import Optional, List
from agents.llm_response_generator import LLMResponseGenerator
from agents.schema import TicketResponse


class ResponseAgent:
    """
    Response Agent: Generates AI draft responses using LLM.
    
    Features:
    - LLM-based response generation
    - KB integration
    - Quality scoring
    - Human review flag
    """

    def __init__(self, llm_generator: Optional[LLMResponseGenerator] = None):
        self.generator = llm_generator or LLMResponseGenerator()

    def generate_response(self, ticket_text: str, category: str, kb_articles: List[str] = None) -> str:
        """
        Generate a response based on ticket category.
        
        Args:
            ticket_text: The customer's ticket message
            category: The classified category
            kb_articles: Optional list of KB articles to reference
            
        Returns:
            Draft response text
        """
        result = self.generator.generate(ticket_text, category, kb_articles)
        return result.response_text

    def evaluate_quality(self, response_text: str) -> float:
        """
        Evaluate response quality (0.0 to 1.0).
        
        Args:
            response_text: The generated response
            
        Returns:
            Quality score between 0.0 and 1.0
        """
        return self.generator.evaluate_quality(response_text)

    def should_human_review(self, response_text: str) -> bool:
        """
        Determine if response needs human review.
        
        Args:
            response_text: The generated response
            
        Returns:
            True if quality score < 0.7
        """
        quality = self.evaluate_quality(response_text)
        return self.generator.should_human_review(quality)
