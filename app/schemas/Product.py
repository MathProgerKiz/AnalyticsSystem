

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.brand import BrandRead
from app.schemas.product_type import ProductTypeRead


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=64)
    description: str | None = None
    price: Decimal
    brand_id: int
    product_type_id: int
    

class ProductCreate(ProductBase):
    pass 

class ProductUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=64)
    description: str | None = None
    price: Decimal | None = None
    brand_id: int | None = None
    product_type_id: int | None = None

class ProductDelete(BaseModel):
    id:int 

class ProductRead(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    brand: BrandRead
    product_type: ProductTypeRead
