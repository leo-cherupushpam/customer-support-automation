# Pydantic v2 request/response models for the FastAPI backend

from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional, List


# ── Request models ──────────────────────────────────────────────────────────

class TicketRequest(BaseModel):
    """Request body for POST /api/tickets"""

    ticket_text: str = Field(..., min_length=1, description="Customer ticket message")

    @field_validator("ticket_text")
    @classmethod
    def ticket_text_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("ticket_text must not be blank")
        return v


# ── Response models ─────────────────────────────────────────────────────────

class TicketResponse(BaseModel):
    """Response body for POST /api/tickets"""

    ticket_id: str
    category: str
    confidence: float
    auto_responded: bool
    response: str
    quality_score: Optional[float] = None
    priority: Optional[str] = None
    escalation: Optional[dict] = None


class TicketSummary(BaseModel):
    """A single ticket in the history list"""

    model_config = ConfigDict(extra="ignore")

    ticket_id: str
    ticket_text: str
    category: str
    response: str
    auto_responded: bool
    confidence: float
    priority: Optional[str] = None
    quality_score: Optional[float] = None


class TicketsListResponse(BaseModel):
    """Response body for GET /api/tickets"""

    tickets: List[TicketSummary]


class AnalyticsResponse(BaseModel):
    """Response body for GET /api/analytics"""

    total_tickets: int
    deflection_rate: float
    average_response_time: float
    estimated_cost: float
    category_distribution: dict
