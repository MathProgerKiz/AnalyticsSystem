from decimal import Decimal

from pydantic import BaseModel


class AnalyticsSchema(BaseModel):
    query: str


class BrandSalesAnalyticsRead(BaseModel):
    brand_id: int
    brand: str
    total_quantity: int
    total_revenue: Decimal


class ProductTypeSalesAnalyticsRead(BaseModel):
    product_type_id: int
    type: str
    total_quantity: int
    total_revenue: Decimal
