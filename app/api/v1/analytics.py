
from fastapi import APIRouter

from app.schemas.analytics import AnalyticsSchema
from app.services.analytics import AnalyticsService



router = APIRouter(
    prefix="/analytics",
    tags=["analytics"]
)


@router.post("/query")
async def quury_analytics(prompt: AnalyticsSchema) -> str:
    return await AnalyticsService.query(prompt.query)