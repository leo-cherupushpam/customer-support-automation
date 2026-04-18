# Learning Agent - Learns from resolved tickets to improve KB

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from src.knowledge_base.kb_manager import KBManager

@dataclass
class KBUpdate:
    """Represents a suggested knowledge base update"""
    question: str
    answer: str
    category: str
    confidence: float
    source_ticket: str
    suggested_filename: str
    review_status: str  # pending, approved, rejected

class LearningAgent:
    """
    Learning Agent: Learns from resolved tickets to improve KB and models.
    
    Features:
    - Daily batch processing
    - New question detection
    - KB auto-update suggestions
    - Pattern detection
    """
    
    def __init__(self):
        # Track processed tickets to avoid duplicates
        self.processed_tickets = set()
        # Initialize KBManager for KB operations
        self.kb_manager = KBManager()
        
    def analyze_resolved_tickets(self, resolved_tickets: List[dict]) -> List[KBUpdate]:
        """
        Analyze resolved tickets and suggest KB updates.
        
        Args:
            resolved_tickets: List of resolved tickets with format:
                {
                    "ticket": str,
                    "response": str,
                    "category": str
                }
            
        Returns:
            List of KBUpdate suggestions
        """
        updates = []
        
        for ticket in resolved_tickets:
            # Skip if already processed
            ticket_key = self._hash_ticket(ticket)
            if ticket_key in self.processed_tickets:
                continue
            
            # Generate KB update if appropriate
            update = self._create_kb_update(ticket)
            if update:
                updates.append(update)
            
            # Mark as processed
            self.processed_tickets.add(ticket_key)
        
        return updates
    
    def _hash_ticket(self, ticket: dict) -> str:
        """Create a hash of the ticket to track processed tickets."""
        return hash(f"{ticket['ticket']}_{ticket['category']}")
    
    def _create_kb_update(self, ticket: dict) -> Optional[KBUpdate]:
        """Create a KB update from a resolved ticket."""
        ticket_text = ticket['ticket'].strip()
        response = ticket['response'].strip()
        category = ticket['category']

        # Skip very short tickets
        if len(ticket_text) < 10 or len(response) < 10:
            return None

        # Calculate confidence based on clarity
        confidence = self._calculate_update_confidence(ticket_text, response)

        # Generate suggested filename from question
        import re
        suggested_filename = re.sub(r'[^\w\s-]', '', ticket_text.lower())
        suggested_filename = re.sub(r'[-\s]+', '-', suggested_filename).strip('-')
        if not suggested_filename:
            suggested_filename = "kb-article"
        suggested_filename = f"{suggested_filename}.md"

        return KBUpdate(
            question=ticket_text,
            answer=response,
            category=category,
            confidence=confidence,
            source_ticket=ticket_text[:50] + "..." if len(ticket_text) > 50 else ticket_text,
            suggested_filename=suggested_filename,
            review_status="pending"
        )
    
    def _calculate_update_confidence(self, ticket_text: str, response: str) -> float:
        """Calculate confidence score for KB update."""
        confidence = 0.5  # Base confidence
        
        # Boost for clear questions
        if ticket_text.endswith('?'):
            confidence += 0.1
        
        # Boost for detailed responses
        if len(response.split()) > 10:
            confidence += 0.1
        
        # Boost for helpful phrases
        helpful_phrases = ['thank', 'please', 'help', 'guide']
        if any(phrase in response.lower() for phrase in helpful_phrases):
            confidence += 0.05
        
        return min(1.0, confidence)
    
    def detect_trending_issues(self, resolved_tickets: List[dict]) -> List[str]:
        """
        Detect trending issues from resolved tickets.
        
        Args:
            resolved_tickets: List of resolved tickets
            
        Returns:
            List of trending issue categories
        """
        category_counts = {}
        
        for ticket in resolved_tickets:
            category = ticket['category']
            category_counts[category] = category_counts.get(category, 0) + 1
        
        # Return categories with 2+ occurrences
        trending = [cat for cat, count in category_counts.items() if count >= 2]
        
        return trending
    
    def schedule_daily_batch(self) -> bool:
        """
        Schedule daily batch processing.
        
        Returns:
            True if batch is scheduled
        """
        # MVP: Always return True
        # In production: Integrate with task scheduler
        return True
