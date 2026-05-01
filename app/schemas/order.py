from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.order_item import OrderItemCreateNested, OrderItemRead


class OrderBase(BaseModel):
    total_price: Decimal = Field(..., ge=0)


class OrderCreate(OrderBase):
    items: list[OrderItemCreateNested] = Field(default_factory=list)


class OrderUpdate(BaseModel):
    total_price: Decimal | None = Field(None, ge=0)
    items: list[OrderItemCreateNested] | None = None


class OrderDelete(BaseModel):
    id: int


class OrderRead(OrderBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_date: datetime
    items: list[OrderItemRead] = Field(default_factory=list)
