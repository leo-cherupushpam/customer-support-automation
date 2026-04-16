# Triage Agent - Classifies tickets and assigns confidence scores

from dataclasses import dataclass
from typing import Optional

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
    Triage Agent: Classifies incoming tickets and assigns confidence scores.
    
    Categories:
    - password_reset: User needs to reset password
    - billing_inquiry: Questions about charges or payments
    - feature_request: Suggestions for new features
    - technical_issue: Bugs or technical problems
    - general_inquiry: General questions
    """
    
    def __init__(self):
        # Simple keyword-based classification for MVP
        # In production, use LLM with few-shot prompting
        self.category_keywords = {
            'password_reset': ['password', 'reset', 'forgot', 'login'],
            'billing_inquiry': ['charge', 'billing', 'payment', 'refund', 'invoice', 'charged'],
            'feature_request': ['feature', 'suggestion', 'wish', 'would love', 'would like'],
            'technical_issue': ['bug', 'error', 'not working', 'broken'],
            'general_inquiry': ['how', 'what', 'when', 'where']
        }
    
    def classify_ticket(self, ticket_text: str) -> ClassificationResult:
        """
        Classify a ticket and return category with confidence score.
        
        Args:
            ticket_text: The customer's ticket message
            
        Returns:
            ClassificationResult with category and confidence
        """
        # Normalize input
        text_lower = ticket_text.lower()
        
        # Count keyword matches
        matches = {}
        for category, keywords in self.category_keywords.items():
            match_count = sum(1 for kw in keywords if kw in text_lower)
            matches[category] = match_count
        
        # Find best match
        best_category = max(matches, key=matches.get)
        match_count = matches[best_category]
        
        # Calculate confidence based on keyword density
        # Each keyword adds ~25% confidence to reach thresholds
        confidence = min(1.0, match_count * 0.25)
        
        # Adjust confidence based on ticket clarity
        if '?' in ticket_text:
            confidence = min(1.0, confidence + 0.15)  # Clear questions get higher confidence
        
        # Boost confidence for clear, specific tickets with multiple keywords
        if match_count >= 2:
            confidence = min(1.0, confidence + 0.25)
        
        # Lower confidence for ambiguous/short tickets
        if len(ticket_text.split()) < 5:
            confidence = confidence * 0.7
        
        return ClassificationResult(
            category=best_category,
            confidence=round(confidence, 2)
        )
