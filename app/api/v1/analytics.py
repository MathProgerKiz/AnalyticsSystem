
import datetime

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Query

from app.analytics.analytics_repositories import AnalyticsRepository
from app.schemas.analytics import (
    AnalyticsSchema,
    BrandSalesAnalyticsRead,
    ProductTypeSalesAnalyticsRead,
)
from app.services.analytics import AnalyticsService



router = APIRouter(
    prefix="/analytics",
    tags=["analytics"]
)


@router.post("/query")
@inject
async def quury_analytics(
    prompt: AnalyticsSchema,
    analytics_repository: FromDishka[AnalyticsRepository],
) -> str:
    return await AnalyticsService.query(prompt.query, analytics_repository)


@router.get("/brands/top", response_model=list[BrandSalesAnalyticsRead])
@inject
async def get_top_selling_brands(
    analytics_repository: FromDishka[AnalyticsRepository],
    limit: int = Query(default=10, ge=1),
):
    return await analytics_repository.get_top_selling_products_by_brand(limit=limit)


@router.get("/product-types/top", response_model=list[ProductTypeSalesAnalyticsRead])
@inject
async def get_top_selling_product_types(
    analytics_repository: FromDishka[AnalyticsRepository],
    limit: int = Query(default=10, ge=1),
):
    return await analytics_repository.get_top_selling_products_by_type(limit=limit)


@router.get("/brands/sales", response_model=list[BrandSalesAnalyticsRead])
@inject
async def get_brand_sales_by_period(
    analytics_repository: FromDishka[AnalyticsRepository],
    start_date: datetime.datetime,
    end_date: datetime.datetime,
):
    return await analytics_repository.get_sales_brand_by_period(
        start_date=start_date,
        end_date=end_date,
    )


@router.get("/product-types/sales", response_model=list[ProductTypeSalesAnalyticsRead])
@inject
async def get_product_type_sales_by_period(
    analytics_repository: FromDishka[AnalyticsRepository],
    start_date: datetime.datetime,
    end_date: datetime.datetime,
):
    return await analytics_repository.get_sales_type_by_period(
        start_date=start_date,
        end_date=end_date,
    )
