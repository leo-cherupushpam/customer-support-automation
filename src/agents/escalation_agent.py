# Escalation Agent - Routes low-confidence tickets to human support

from dataclasses import dataclass
from typing import Optional

@dataclass
class EscalationTicket:
    """Represents an escalated ticket for human review"""
    context_summary: str
    suggested_response: str
    priority: str  # 'low', 'medium', 'high', 'urgent'
    original_ticket: str
    category: str
    confidence: float

class EscalationAgent:
    """
    Escalation Agent: Routes low-confidence tickets to human support with context.
    
    Features:
    - Context summary generation
    - Suggested response draft
    - Priority scoring
    """
    
    def __init__(self):
        # Priority boost keywords
        self.urgent_keywords = ['urgent', 'immediately', 'asap', 'emergency', 'locked', 'cannot access']
        self.high_priority_keywords = ['refund', 'charged', 'billing', 'error', 'bug']
        
    def create_escalation(self, ticket_text: str, category: str, confidence: float) -> EscalationTicket:
        """
        Create an escalation ticket for human review.
        
        Args:
            ticket_text: Original ticket text
            category: Classified category
            confidence: Confidence score from triage
            
        Returns:
            EscalationTicket with context, suggested response, and priority
        """
        # Generate context summary
        context_summary = self._generate_context_summary(ticket_text, category, confidence)
        
        # Generate suggested response
        suggested_response = self._generate_suggested_response(ticket_text, category)
        
        # Assign priority
        priority = self._assign_priority(ticket_text, category, confidence)
        
        return EscalationTicket(
            context_summary=context_summary,
            suggested_response=suggested_response,
            priority=priority,
            original_ticket=ticket_text,
            category=category,
            confidence=confidence
        )
    
    def _generate_context_summary(self, ticket_text: str, category: str, confidence: float) -> str:
        """Generate a brief context summary for the human agent."""
        # Truncate long tickets
        summary_text = ticket_text[:200] + "..." if len(ticket_text) > 200 else ticket_text
        
        return (
            f"Category: {category}\n"
            f"Confidence: {confidence:.0%}\n"
            f"Customer message: {summary_text}"
        )
    
    def _generate_suggested_response(self, ticket_text: str, category: str) -> str:
        """Generate a suggested response draft for human to edit."""
        # Simple templates for MVP
        templates = {
            'password_reset': "Thank you for contacting us about your password. Let me help you reset it...",
            'billing_inquiry': "Thank you for reaching out about your billing question. I'll look into this for you...",
            'feature_request': "Thank you for your feature suggestion! I'll forward this to our product team...",
            'technical_issue': "I'm sorry to hear you're experiencing technical issues. Let me investigate this...",
            'general_inquiry': "Thank you for your inquiry. I'll be happy to help you with this..."
        }
        
        return templates.get(category, templates['general_inquiry'])
    
    def _assign_priority(self, ticket_text: str, category: str, confidence: float) -> str:
        """Assign priority based on urgency keywords and confidence."""
        text_lower = ticket_text.lower()
        
        # Check for urgent keywords
        has_urgent = any(keyword in text_lower for keyword in self.urgent_keywords)
        has_high_priority = any(keyword in text_lower for keyword in self.high_priority_keywords)
        
        # Priority logic
        if has_urgent or confidence < 0.5:
            return 'urgent'
        elif has_high_priority or confidence < 0.65:
            return 'high'
        elif confidence < 0.80:
            return 'medium'
        else:
            return 'low'
