

from decimal import Decimal

from pydantic import BaseModel

from app.schemas.brand import BrandRead
from app.schemas.product_type import ProductTypeRead


class ProductBase(BaseModel):
    name: str
    description: str
    price: Decimal 
    

class ProductCreate(ProductBase):
    pass 

class ProductUpdate(ProductBase):
    pass 

class ProductDelete(BaseModel):
    id:int 

class ProductRead(ProductBase):
    id: int
    brand: BrandRead
    product_type: ProductTypeRead
