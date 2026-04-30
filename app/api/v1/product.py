

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, HTTPException, status

from app.schemas.Product import ProductCreate, ProductRead, ProductUpdate
from app.services.product import ProductService


router = APIRouter(
    prefix="/products",
    tags=["products"]
)


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
@inject
async def create_product(
    product: ProductCreate,
    service: FromDishka[ProductService]
):
    return await service.create_product(product.model_dump())

@router.get("/", response_model=list[ProductRead])
@inject
async def get_products(
    service: FromDishka[ProductService]
):
    return await service.get_products()

@router.get("/{product_id}", response_model=ProductRead)
@inject
async def get_product(
    product_id: int,
    service: FromDishka[ProductService]
):
    product = await service.get_product(product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return product

@router.patch("/{product_id}", response_model=ProductRead)
@inject
async def update_product(
    product_id: int,
    product: ProductUpdate,
    service: FromDishka[ProductService]
):
    updated_product = await service.update_product(
        product_id,
        product.model_dump(exclude_unset=True),
    )
    if updated_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return updated_product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_product(
    product_id: int,
    service: FromDishka[ProductService]
):
    deleted_product = await service.delete_product(product_id)
    if deleted_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
