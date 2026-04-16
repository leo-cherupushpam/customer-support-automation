# Classification prompt templates

from typing import List


CLASSIFICATION_SYSTEM_PROMPT = """You are a customer support ticket classifier. Analyze the ticket and return a JSON object with the following fields:

- category: One of these categories: password_reset, billing_inquiry, feature_request, technical_issue, general_inquiry
- priority: Integer 1-5 (1=low, 5=critical)
- sentiment: One of: positive, neutral, negative
- confidence: Float 0.0-1.0 representing model confidence
- reasoning: Brief explanation of your classification

Return ONLY valid JSON, no markdown or extra text."""


def get_classification_prompt(
    ticket_text: str, categories: List[str] = None
) -> List[dict]:
    """Get classification prompt with ticket context"""
    categories_str = (
        ", ".join(categories)
        if categories
        else "password_reset, billing_inquiry, feature_request, technical_issue, general_inquiry"
    )

    return [
        {
            "role": "system",
            "content": CLASSIFICATION_SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": f"Categories: {categories_str}\n\nTicket: {ticket_text}",
        },
    ]
