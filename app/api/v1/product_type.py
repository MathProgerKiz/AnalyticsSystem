from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status

from app.schemas.product_type import ProductTypeCreate, ProductTypeRead
from app.services.product_type import ProductTypeService


router = APIRouter(
    prefix="/product-types",
    tags=["product types"],
)


@router.post("/", response_model=ProductTypeRead, status_code=status.HTTP_201_CREATED)
@inject
async def create_product_type(
    product_type: ProductTypeCreate,
    service: FromDishka[ProductTypeService],
):
    return await service.create_product_type(product_type.model_dump())
