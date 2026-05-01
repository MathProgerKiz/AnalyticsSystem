from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, HTTPException, status

from app.schemas.product_type import (
    ProductTypeCreate,
    ProductTypeRead,
    ProductTypeUpdate,
)
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


@router.get("/", response_model=list[ProductTypeRead])
@inject
async def get_product_types(
    service: FromDishka[ProductTypeService],
):
    return await service.get_product_types()


@router.get("/{product_type_id}", response_model=ProductTypeRead)
@inject
async def get_product_type(
    product_type_id: int,
    service: FromDishka[ProductTypeService],
):
    product_type = await service.get_product_type(product_type_id)
    if product_type is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product type not found",
        )
    return product_type


@router.patch("/{product_type_id}", response_model=ProductTypeRead)
@inject
async def update_product_type(
    product_type_id: int,
    product_type: ProductTypeUpdate,
    service: FromDishka[ProductTypeService],
):
    updated_product_type = await service.update_product_type(
        product_type_id,
        product_type.model_dump(exclude_unset=True),
    )
    if updated_product_type is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product type not found",
        )
    return updated_product_type


@router.delete("/{product_type_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_product_type(
    product_type_id: int,
    service: FromDishka[ProductTypeService],
):
    deleted_product_type = await service.delete_product_type(product_type_id)
    if deleted_product_type is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product type not found",
        )
