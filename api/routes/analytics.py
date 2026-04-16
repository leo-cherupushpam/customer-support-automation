# Analytics router — GET /api/analytics

from fastapi import APIRouter, HTTPException, Request

from api.models import AnalyticsResponse

router = APIRouter()


@router.get("", response_model=AnalyticsResponse)
async def get_analytics(request: Request) -> AnalyticsResponse:
    """Return current analytics statistics."""
    try:
        stats = request.app.state.analytics.get_stats()
        return AnalyticsResponse(
            total_tickets=stats["total_tickets"],
            deflection_rate=stats["deflection_rate"],
            average_response_time=stats["average_response_time"],
            estimated_cost=stats["estimated_cost"],
            category_distribution=stats["category_distribution"],
        )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Analytics unavailable")
