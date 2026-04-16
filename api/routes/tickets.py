# Tickets router — POST /api/tickets, GET /api/tickets

import uuid
from typing import List

from fastapi import APIRouter, Request

from api.models import TicketRequest, TicketResponse, TicketSummary, TicketsListResponse

router = APIRouter()

_TICKET_HISTORY_LIMIT = 20


@router.post("", response_model=TicketResponse, status_code=200)
async def process_ticket(body: TicketRequest, request: Request) -> TicketResponse:
    """
    Classify an incoming support ticket and either auto-respond or escalate.

    Flow (mirrors app.py):
      1. TriageAgent classifies the ticket.
      2. If confidence > 85 % → ResponseAgent generates a response.
      3. Otherwise → EscalationAgent creates an escalation ticket.
      4. Record in AnalyticsTracker and append to in-memory history.
    """
    state = request.app.state

    ticket_id = str(uuid.uuid4())[:8]
    ticket_text = body.ticket_text

    # Step 1: Triage
    classification = state.triage_agent.classify_ticket(ticket_text)

    # Step 2: Route
    if classification.should_auto_respond():
        response_text = state.response_agent.generate_response(ticket_text, classification.category)
        quality_score = state.response_agent.evaluate_quality(response_text)

        state.analytics.track_ticket_processed(
            ticket_id=ticket_id,
            category=classification.category,
            auto_responded=True,
            confidence=classification.confidence,
            tokens_used=200,
            response_time=0.5,
        )

        record: dict = {
            "ticket_id": ticket_id,
            "ticket_text": ticket_text,
            "category": classification.category,
            "response": response_text,
            "auto_responded": True,
            "confidence": classification.confidence,
            "priority": "low",
            "quality_score": quality_score,
        }
        state.ticket_history.append(record)

        return TicketResponse(
            ticket_id=ticket_id,
            category=classification.category,
            confidence=classification.confidence,
            auto_responded=True,
            response=response_text,
            quality_score=quality_score,
        )

    else:
        escalation = state.escalation_agent.create_escalation(
            ticket_text,
            classification.category,
            classification.confidence,
        )

        state.analytics.track_ticket_processed(
            ticket_id=ticket_id,
            category=classification.category,
            auto_responded=False,
            confidence=classification.confidence,
            tokens_used=150,
            response_time=0.5,
        )

        record = {
            "ticket_id": ticket_id,
            "ticket_text": ticket_text,
            "category": classification.category,
            "response": escalation.suggested_response,
            "auto_responded": False,
            "confidence": classification.confidence,
            "priority": escalation.priority,
        }
        state.ticket_history.append(record)

        return TicketResponse(
            ticket_id=ticket_id,
            category=classification.category,
            confidence=classification.confidence,
            auto_responded=False,
            response=escalation.suggested_response,
            priority=escalation.priority,
            escalation={
                "context_summary": escalation.context_summary,
                "suggested_response": escalation.suggested_response,
                "priority": escalation.priority,
            },
        )


@router.get("", response_model=TicketsListResponse)
async def list_tickets(request: Request) -> TicketsListResponse:
    """Return the last 20 processed tickets."""
    history: List[dict] = request.app.state.ticket_history
    recent = history[-_TICKET_HISTORY_LIMIT:]
    tickets = [TicketSummary(**t) for t in recent]
    return TicketsListResponse(tickets=tickets)
