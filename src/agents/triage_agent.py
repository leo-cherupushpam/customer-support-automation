# Triage Agent - Classifies tickets using LLM

from dataclasses import dataclass
from typing import Optional
from agents.llm_classifier import LLMClassifier
from agents.schema import TicketClassification

@dataclass
class ClassificationResult:
    """Result of ticket classification"""
    category: str
    confidence: float  # 0.0 to 1.0
    
    def should_auto_respond(self) -> bool:
        """Return True if confidence > 85%"""
        return self.confidence > 0.85

class TriageAgent:
    """
    Triage Agent: Classifies incoming tickets using LLM.
    
    Categories:
    - password_reset: User needs to reset password
    - billing_inquiry: Questions about charges or payments
    - feature_request: Suggestions for new features
    - technical_issue: Bugs or technical problems
    - general_inquiry: General questions
    """
    
    def __init__(self, llm_classifier: Optional[LLMClassifier] = None):
        self.classifier = llm_classifier or LLMClassifier()
    
    def classify_ticket(self, ticket_text: str) -> ClassificationResult:
        """
        Classify a ticket using LLM and return category with confidence.
        
        Args:
            ticket_text: The customer's ticket message
            
        Returns:
            ClassificationResult with category and confidence
        """
        # Use LLM classifier
        llm_result = self.classifier.classify(ticket_text)
        
        return ClassificationResult(
            category=llm_result.category,
            confidence=llm_result.confidence
        )
