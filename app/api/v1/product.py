


from typing import Annotated

from fastapi import APIRouter

from app.schemas.Product import ProductCreate
from app.services.product import ProductService


router = APIRouter(
    prefix="/products",
    tags=["products"]
)


# @router.post('/create')
# async def create_product(
#     product: ProductCreate
#     service:Annotated[ProductService, ]
                        
#                         ):
#     pass