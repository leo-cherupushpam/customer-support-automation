# Response prompt templates

from typing import List


RESPONSE_SYSTEM_PROMPT = """You are a customer support response generator. Generate a helpful, empathetic response to the customer ticket.

Requirements:
- Be friendly and professional
- Address the customer's specific issue
- Include relevant knowledge base citations if applicable
- Keep response concise (under 200 words)
- If the response needs human review, set needs_human_review to true

Return ONLY valid JSON with these fields:
- response_text: The response content
- citations: List of citation IDs (e.g., ["KB-001"])
- quality_score: Float 0.0-1.0
- needs_human_review: Boolean"""


def get_response_prompt(
    ticket_text: str, category: str, kb_articles: List[str] = None
) -> List[dict]:
    """Get response prompt with context"""
    kb_context = (
        "\n\nAvailable KB Articles:\n" + "\n".join(kb_articles)
        if kb_articles
        else ""
    )

    return [
        {
            "role": "system",
            "content": RESPONSE_SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": f"Category: {category}\n\nTicket: {ticket_text}{kb_context}",
        },
    ]
