from pydantic import BaseModel, ConfigDict, Field

from app.schemas.Product import ProductRead


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)


class OrderItemCreate(OrderItemBase):
    order_id: int


class OrderItemCreateNested(OrderItemBase):
    pass


class OrderItemUpdate(BaseModel):
    product_id: int | None = None
    quantity: int | None = Field(None, gt=0)


class OrderItemDelete(BaseModel):
    id: int


class OrderItemRead(OrderItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_id: int
    product: ProductRead
