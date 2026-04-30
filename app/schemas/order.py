from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.order_item import OrderItemCreateNested, OrderItemRead


class OrderBase(BaseModel):
    status: str = Field(default="created", min_length=1, max_length=32)


class OrderCreate(OrderBase):
    items: list[OrderItemCreateNested] = Field(default_factory=list)


class OrderUpdate(BaseModel):
    status: str | None = Field(None, min_length=1, max_length=32)
    items: list[OrderItemCreateNested] | None = None


class OrderDelete(BaseModel):
    id: int


class OrderRead(OrderBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
    items: list[OrderItemRead] = Field(default_factory=list)
