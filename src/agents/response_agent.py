# Response Agent - Generates responses with KB lookup

from typing import Optional, List, Dict

class ResponseAgent:
    """
    Response Agent: Generates AI draft responses with knowledge base citations.
    
    MVP Implementation:
    - Simple template-based responses for MVP
    - In production: RAG with semantic search + LLM generation
    """
    
    def __init__(self):
        # Simple template-based knowledge base for MVP
        self.kb_templates = {
            'password_reset': """To reset your password:
1. Go to the login page
2. Click "Forgot Password"
3. Enter your email address
4. Check your email for reset link
5. Follow the link to create new password

If you don't receive the email within 5 minutes, check your spam folder.

**Citation**: KB-001: Password Reset Guide""",
            
            'billing_inquiry': """Thank you for contacting us about your billing question.

For billing inquiries, we'll need to verify your account first. Please provide:
- Your account email
- Last 4 digits of payment method
- Description of the issue

Our billing team will respond within 24-48 hours.

**Citation**: KB-002: Billing Support Process""",
            
            'feature_request': """Thank you for your feature suggestion!

We appreciate feedback from users like you. Your request has been logged and will be reviewed by our product team.

To track similar features and vote on upcoming releases, visit our [Feature Requests Board].

**Citation**: KB-003: Feature Request Process""",
            
            'technical_issue': """I'm sorry to hear you're experiencing technical issues.

To help us investigate:
- What browser/device are you using?
- When did the issue start?
- Are you seeing any error messages?
- Can you provide screenshots?

Our technical team will investigate and respond within 24 hours.

**Citation**: KB-004: Technical Support Process""",
            
            'general_inquiry': """Thank you for your inquiry!

I'll be happy to help you with this question. Our team is reviewing your request and will provide a detailed response within 24-48 hours.

If this is urgent, please call our support line at [phone number].

**Citation**: KB-005: General Inquiry Process"""
        }
    
    def generate_response(self, ticket_text: str, category: str) -> str:
        """
        Generate a response based on ticket category.
        
        Args:
            ticket_text: The customer's ticket message
            category: The classified category
            
        Returns:
            Draft response with KB citations
        """
        # Get template for category
        template = self.kb_templates.get(category, self.kb_templates['general_inquiry'])
        
        # For MVP, return template as-is
        # In production: Use LLM to personalize based on ticket_text
        return template
    
    def evaluate_quality(self, response: str) -> float:
        """
        Evaluate response quality (0.0 to 1.0).
        
        MVP: Simple heuristic based on length and citation presence
        
        Args:
            response: The generated response
            
        Returns:
            Quality score between 0.0 and 1.0
        """
        if not response or len(response) < 20:
            return 0.0
        
        # Base score from length
        length_score = min(1.0, len(response) / 200)
        
        # Bonus for citations
        citation_score = 0.2 if "citation" in response.lower() else 0.0
        
        # Bonus for helpful phrases
        helpful_phrases = ['thank you', 'please', 'help', 'support']
        phrase_score = sum(1 for phrase in helpful_phrases if phrase in response.lower()) * 0.05
        
        return min(1.0, length_score + citation_score + phrase_score)
    
    def should_human_review(self, quality_score: float) -> bool:
        """
        Determine if response needs human review.
        
        Args:
            quality_score: The quality score from evaluate_quality()
            
        Returns:
            True if quality score < 0.7 (needs review)
        """
        return quality_score < 0.7
