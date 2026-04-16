# Tests for the FastAPI backend (api/)

import sys
import os

# Ensure the project root and src/ are on the path (mirrors api/main.py setup)
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SRC = os.path.join(_ROOT, "src")
for _p in (_ROOT, _SRC):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient

from api.main import create_app
from src.agents.triage_agent import ClassificationResult
from src.agents.escalation_agent import EscalationTicket
from utils.analytics import AnalyticsTracker


# ── Helpers ───────────────────────────────────────────────────────────────────

def _make_mock_triage(category: str, confidence: float) -> MagicMock:
    agent = MagicMock()
    agent.classify_ticket.return_value = ClassificationResult(
        category=category,
        confidence=confidence,
    )
    return agent


def _make_mock_response(response_text: str = "Here is how to reset your password.") -> MagicMock:
    agent = MagicMock()
    agent.generate_response.return_value = response_text
    agent.evaluate_quality.return_value = 0.92
    return agent


def _make_mock_escalation(priority: str = "high") -> MagicMock:
    agent = MagicMock()
    agent.create_escalation.return_value = EscalationTicket(
        context_summary="Priority: HIGH\nCategory: general_inquiry\nConfidence: 50%\nCustomer message: Something vague",
        suggested_response="Thank you for your inquiry. I'll be happy to help you with this...",
        priority=priority,
        original_ticket="Something vague",
        category="general_inquiry",
        confidence=0.50,
    )
    return agent


def _make_mock_analytics() -> MagicMock:
    tracker = MagicMock(spec=AnalyticsTracker)
    tracker.get_stats.return_value = {
        "total_tickets": 5,
        "auto_responded": 3,
        "escalated": 2,
        "total_tokens": 1000,
        "total_response_time": 2.5,
        "category_distribution": {"password_reset": 3, "general_inquiry": 2},
        "last_updated": None,
        "deflection_rate": 0.6,
        "average_response_time": 0.5,
        "estimated_cost": 0.0001,
    }
    return tracker


def _make_test_client(
    triage_agent=None,
    response_agent=None,
    escalation_agent=None,
    analytics=None,
) -> TestClient:
    """Create a TestClient with injected mock singletons."""
    app = create_app()

    app.state.triage_agent = triage_agent or _make_mock_triage("password_reset", 0.95)
    app.state.response_agent = response_agent or _make_mock_response()
    app.state.escalation_agent = escalation_agent or _make_mock_escalation()
    app.state.analytics = analytics or _make_mock_analytics()
    app.state.ticket_history = []

    return TestClient(app)


# ── Tests ─────────────────────────────────────────────────────────────────────

class TestPostTickets:
    """POST /api/tickets"""

    def test_password_reset_auto_responded(self):
        """High-confidence password-reset ticket should be auto-responded."""
        client = _make_test_client(
            triage_agent=_make_mock_triage("password_reset", 0.95),
            response_agent=_make_mock_response("Here is how to reset your password."),
        )

        resp = client.post("/api/tickets", json={"ticket_text": "I forgot my password and cannot log in."})

        assert resp.status_code == 200
        data = resp.json()
        assert data["auto_responded"] is True
        assert data["category"] == "password_reset"
        assert data["confidence"] == pytest.approx(0.95)
        assert "ticket_id" in data
        assert data["response"] != ""
        assert data["quality_score"] is not None

    def test_empty_ticket_text_returns_422(self):
        """Blank ticket_text should fail Pydantic validation with 422."""
        client = _make_test_client()

        # Completely empty string — violates min_length=1
        resp = client.post("/api/tickets", json={"ticket_text": ""})
        assert resp.status_code == 422

    def test_whitespace_only_ticket_text_returns_422(self):
        """Whitespace-only ticket_text should also fail validation with 422."""
        client = _make_test_client()

        resp = client.post("/api/tickets", json={"ticket_text": "   "})
        assert resp.status_code == 422

    def test_vague_ticket_escalates(self):
        """Low-confidence vague ticket should be escalated (auto_responded=False)."""
        client = _make_test_client(
            triage_agent=_make_mock_triage("general_inquiry", 0.50),
            escalation_agent=_make_mock_escalation("high"),
        )

        resp = client.post("/api/tickets", json={"ticket_text": "Something isn't working right."})

        assert resp.status_code == 200
        data = resp.json()
        assert data["auto_responded"] is False
        assert "priority" in data
        assert data["priority"] is not None
        assert "escalation" in data
        assert data["escalation"] is not None
        # Response shape must include the expected keys
        assert "ticket_id" in data
        assert "category" in data
        assert "confidence" in data
        assert "response" in data


class TestGetTickets:
    """GET /api/tickets"""

    def test_returns_ticket_list(self):
        """GET /api/tickets should return a list (possibly empty)."""
        client = _make_test_client()

        resp = client.get("/api/tickets")

        assert resp.status_code == 200
        data = resp.json()
        assert "tickets" in data
        assert isinstance(data["tickets"], list)

    def test_returns_processed_tickets(self):
        """Processed tickets should appear in GET /api/tickets."""
        client = _make_test_client(
            triage_agent=_make_mock_triage("password_reset", 0.95),
            response_agent=_make_mock_response("Reset your password here."),
        )

        # Process a ticket first
        client.post("/api/tickets", json={"ticket_text": "Reset my password please."})

        resp = client.get("/api/tickets")
        data = resp.json()
        assert len(data["tickets"]) == 1
        assert data["tickets"][0]["category"] == "password_reset"

    def test_max_20_tickets_returned(self):
        """GET /api/tickets should return at most 20 tickets."""
        client = _make_test_client(
            triage_agent=_make_mock_triage("password_reset", 0.95),
            response_agent=_make_mock_response("Here is help."),
        )

        for _ in range(25):
            client.post("/api/tickets", json={"ticket_text": "Reset my password."})

        resp = client.get("/api/tickets")
        data = resp.json()
        assert len(data["tickets"]) <= 20


class TestGetAnalytics:
    """GET /api/analytics"""

    def test_returns_expected_keys(self):
        """Analytics response must include all required top-level keys."""
        client = _make_test_client(analytics=_make_mock_analytics())

        resp = client.get("/api/analytics")

        assert resp.status_code == 200
        data = resp.json()

        required_keys = {
            "total_tickets",
            "deflection_rate",
            "average_response_time",
            "estimated_cost",
            "category_distribution",
        }
        assert required_keys.issubset(data.keys())

    def test_analytics_values_are_correct_types(self):
        """Analytics values should have correct types."""
        client = _make_test_client(analytics=_make_mock_analytics())

        resp = client.get("/api/analytics")
        data = resp.json()

        assert isinstance(data["total_tickets"], int)
        assert isinstance(data["deflection_rate"], float)
        assert isinstance(data["average_response_time"], float)
        assert isinstance(data["estimated_cost"], float)
        assert isinstance(data["category_distribution"], dict)
