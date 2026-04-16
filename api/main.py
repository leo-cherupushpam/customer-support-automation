# FastAPI application — entry point
#
# Run with:
#   uvicorn api.main:app --port 8000 --reload

import sys
import os

# Ensure the project root is on sys.path so that "src.agents", "utils", etc.
# resolve correctly regardless of working directory.
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

# Also make the src/ sub-package importable as a plain namespace (agents.*).
# The existing code inside src/agents/ imports with `from agents.xxx import …`
# which works only when src/ itself is on sys.path.
_SRC_DIR = os.path.join(_PROJECT_ROOT, "src")
if _SRC_DIR not in sys.path:
    sys.path.insert(0, _SRC_DIR)

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import tickets as tickets_router
from api.routes import analytics as analytics_router

# ── Singletons ───────────────────────────────────────────────────────────────
# Import here (after sys.path is fixed) so TestClient picks up the same state.

from src.agents import TriageAgent, ResponseAgent, EscalationAgent
from utils.analytics import AnalyticsTracker

_triage_agent = TriageAgent()
_response_agent = ResponseAgent()
_escalation_agent = EscalationAgent()
_analytics = AnalyticsTracker("analytics.json")
_ticket_history: list = []

# ── App factory ───────────────────────────────────────────────────────────────

def create_app() -> FastAPI:
    app = FastAPI(
        title="Customer Support Automation API",
        version="1.0.0",
        description="FastAPI backend for the AI customer support automation system.",
    )

    # CORS — allow all origins for local Next.js development
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Attach singletons to app state so routes can access them via request.app.state
    app.state.triage_agent = _triage_agent
    app.state.response_agent = _response_agent
    app.state.escalation_agent = _escalation_agent
    app.state.analytics = _analytics
    app.state.ticket_history = _ticket_history

    # Mount routers
    app.include_router(tickets_router.router, prefix="/api/tickets", tags=["tickets"])
    app.include_router(analytics_router.router, prefix="/api/analytics", tags=["analytics"])

    return app


app = create_app()
