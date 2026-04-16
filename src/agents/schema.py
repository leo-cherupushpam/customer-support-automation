# Agents package - Schemas

from pydantic import BaseModel, Field
from typing import Literal


class TicketClassification(BaseModel):
    """Structured ticket classification"""

    category: str = Field(
        description="The classification category (e.g., password_reset, billing_inquiry)"
    )
    priority: int = Field(
        description="Priority level 1-5 (1=low, 5=critical)", ge=1, le=5
    )
    sentiment: Literal["positive", "neutral", "negative"] = Field(
        description="Customer sentiment"
    )
    confidence: float = Field(
        description="Model confidence 0.0-1.0", ge=0.0, le=1.0
    )
    reasoning: str = Field(description="Brief explanation of classification")


class TicketResponse(BaseModel):
    """Structured ticket response"""

    response_text: str = Field(description="The generated response text")
    citations: list[str] = Field(
        description="List of KB article citations used", default=[]
    )
    quality_score: float = Field(description="Quality score 0.0-1.0", ge=0.0, le=1.0)
    needs_human_review: bool = Field(
        description="True if response needs human review (quality < 0.7)"
    )
