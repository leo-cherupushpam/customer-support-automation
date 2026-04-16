# Analytics tracking for customer support automation

import json
import os
from typing import Dict, Any
from datetime import datetime


class AnalyticsTracker:
    """Track analytics for customer support automation"""

    def __init__(self, file_path: str = "analytics.json"):
        self.file_path = file_path
        self.stats = self._load_stats()

    def _load_stats(self) -> Dict[str, Any]:
        """Load stats from file or initialize empty"""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return self._empty_stats()
        return self._empty_stats()

    def _save_stats(self):
        """Save stats to file"""
        with open(self.file_path, 'w') as f:
            json.dump(self.stats, f, indent=2)

    def _empty_stats(self) -> Dict[str, Any]:
        """Return empty stats structure"""
        return {
            "total_tickets": 0,
            "auto_responded": 0,
            "escalated": 0,
            "total_tokens": 0,
            "total_response_time": 0.0,
            "category_distribution": {},
            "last_updated": None
        }

    def track_ticket_processed(
        self,
        ticket_id: str,
        category: str,
        auto_responded: bool,
        confidence: float,
        tokens_used: int,
        response_time: float
    ):
        """Track a processed ticket"""
        self.stats["total_tickets"] += 1
        
        if auto_responded:
            self.stats["auto_responded"] += 1
        else:
            self.stats["escalated"] += 1
        
        self.stats["total_tokens"] += tokens_used
        self.stats["total_response_time"] += response_time
        
        # Track category distribution
        if category not in self.stats["category_distribution"]:
            self.stats["category_distribution"][category] = 0
        self.stats["category_distribution"][category] += 1
        
        self.stats["last_updated"] = datetime.now().isoformat()
        
        self._save_stats()

    def get_stats(self) -> Dict[str, Any]:
        """Get current statistics"""
        total = self.stats["total_tickets"]
        
        # Calculate derived metrics
        deflection_rate = (
            self.stats["auto_responded"] / total if total > 0 else 0.0
        )
        
        average_response_time = (
            self.stats["total_response_time"] / total if total > 0 else 0.0
        )
        
        # Estimate cost (GPT-4o-mini: $0.15/M input, $0.60/M output)
        # Approx $0.00018 per million tokens
        estimated_cost = self.stats["total_tokens"] * 0.00018 / 1000000
        
        return {
            **self.stats,
            "deflection_rate": round(deflection_rate, 4),
            "average_response_time": round(average_response_time, 3),
            "estimated_cost": round(estimated_cost, 4)
        }

    def reset_stats(self):
        """Reset all statistics"""
        self.stats = self._empty_stats()
        self._save_stats()
