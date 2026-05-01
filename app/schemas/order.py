from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.order_item import OrderItemCreateNested, OrderItemRead


class OrderBase(BaseModel):
    total_price: Decimal = Field(..., ge=0)


class OrderCreate(BaseModel):
    items: list[OrderItemCreateNested] = Field(..., min_length=1)


class OrderUpdate(BaseModel):
    items: list[OrderItemCreateNested] | None = Field(None, min_length=1)


class OrderDelete(BaseModel):
    id: int


class OrderRead(OrderBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_date: datetime
    items: list[OrderItemRead] = Field(default_factory=list)
