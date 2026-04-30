

from dishka import FromDishka
from fastapi import APIRouter

from app.schemas.Product import ProductCreate
from app.services.product import ProductService


router = APIRouter(
    prefix="/products",
    tags=["products"]
)


@router.post('/create')
async def create_product(
    product: ProductCreate,
    service: FromDishka[ProductService]
):
    return await service.create_product(product)

@router.get('/list')
async def get_products(
    service: FromDishka[ProductService]
):
    return await service.get_products()

@router.get('/{product_id}')
async def get_product(
    product_id: int,
    service: FromDishka[ProductService]
):
    return await service.get_product(product_id)

@router.put('/{product_id}')
async def update_product(
    product_id: int,
    product: ProductCreate,
    service: FromDishka[ProductService]
):
    return await service.update_product(product_id, product)