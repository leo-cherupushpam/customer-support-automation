# Template matcher — fast keyword-based routing before RAG

import re
from typing import Dict, Optional, Tuple

# Map template keys to (keywords, canned response)
_TEMPLATES: Dict[str, Dict] = {
    "password_reset": {
        "keywords": ["password", "reset", "forgot", "login", "can't log in", "locked out"],
        "response": (
            "To reset your password:\n"
            "1. Go to the login page and click 'Forgot Password'.\n"
            "2. Enter your registered email and click Send.\n"
            "3. Open the email and click the reset link (valid for 24 hours).\n"
            "4. Choose a new password and log in.\n\n"
            "If you don't receive the email, check your spam folder or contact support."
        ),
    },
    "billing_inquiry": {
        "keywords": ["charge", "charged", "billing", "invoice", "payment", "receipt", "cost", "price"],
        "response": (
            "For billing questions:\n"
            "• View your invoices at Account > Billing > Invoice History.\n"
            "• To dispute a charge, go to Account > Billing > Transaction History and click 'Dispute'.\n"
            "• To update your payment method, go to Account > Billing > Payment Methods.\n\n"
            "Our billing team responds within 2 business days."
        ),
    },
    "refund": {
        "keywords": ["refund", "money back", "cancel charge", "reimburs"],
        "response": (
            "Refund policy:\n"
            "• Monthly plans: refundable within 48 hours if no usage occurred.\n"
            "• Annual plans: pro-rated refund within 14 days.\n"
            "To request a refund, go to Account > Billing > Transaction History and click 'Request Refund'."
        ),
    },
    "technical_issue": {
        "keywords": ["error", "bug", "broken", "not working", "crash", "issue", "problem", "fail"],
        "response": (
            "Quick troubleshooting steps:\n"
            "1. Clear your browser cache and cookies.\n"
            "2. Try a different browser or incognito mode.\n"
            "3. Check our status page at status.example.com.\n"
            "4. Disable browser extensions temporarily.\n\n"
            "If the issue persists, please share your browser, OS version, and a screenshot."
        ),
    },
    "account_management": {
        "keywords": ["account", "profile", "delete account", "close account", "2fa", "two-factor", "notification"],
        "response": (
            "Account management tips:\n"
            "• Update your profile: Account > Profile.\n"
            "• Enable 2FA: Account > Security > Two-Factor Authentication.\n"
            "• Manage notifications: Account > Notifications.\n"
            "• Close your account: Account > Settings > Close Account (data retained 30 days)."
        ),
    },
}


class TemplateMatcher:
    """Keyword-based matcher that returns a canned response when confidence is high."""

    CONFIDENCE_THRESHOLD = 0.6

    def match(self, ticket_text: str) -> Tuple[Optional[str], float]:
        """Return ``(template_key, confidence)`` for the best matching template.

        Confidence is the fraction of the template's keywords found in the text.
        Returns ``(None, 0.0)`` when nothing matches.
        """
        text_lower = ticket_text.lower()
        best_key = None
        best_score = 0.0

        for key, data in _TEMPLATES.items():
            keywords = data["keywords"]
            hits = sum(1 for kw in keywords if kw in text_lower)
            score = hits / len(keywords)
            if score > best_score:
                best_score = score
                best_key = key

        if best_score == 0.0:
            return None, 0.0
        return best_key, best_score

    def get_response(self, template_key: str) -> Optional[str]:
        """Return the canned response for *template_key*, or ``None``."""
        data = _TEMPLATES.get(template_key)
        return data["response"] if data else None

    def try_match(self, ticket_text: str) -> Optional[str]:
        """Return a canned response if confidence >= threshold, else ``None``."""
        key, confidence = self.match(ticket_text)
        if key and confidence >= self.CONFIDENCE_THRESHOLD:
            return self.get_response(key)
        return None
