from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, HTTPException, status

from app.schemas.brand import BrandCreate, BrandRead, BrandUpdate
from app.services.brand import BrandService


router = APIRouter(
    prefix="/brands",
    tags=["brands"],
)


@router.post("/", response_model=BrandRead, status_code=status.HTTP_201_CREATED)
@inject
async def create_brand(
    brand: BrandCreate,
    service: FromDishka[BrandService],
):
    return await service.create_brand(brand.model_dump())


@router.get("/", response_model=list[BrandRead])
@inject
async def get_brands(
    service: FromDishka[BrandService],
):
    return await service.get_brands()


@router.get("/{brand_id}", response_model=BrandRead)
@inject
async def get_brand(
    brand_id: int,
    service: FromDishka[BrandService],
):
    brand = await service.get_brand(brand_id)
    if brand is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand not found",
        )
    return brand


@router.patch("/{brand_id}", response_model=BrandRead)
@inject
async def update_brand(
    brand_id: int,
    brand: BrandUpdate,
    service: FromDishka[BrandService],
):
    updated_brand = await service.update_brand(
        brand_id,
        brand.model_dump(exclude_unset=True),
    )
    if updated_brand is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand not found",
        )
    return updated_brand


@router.delete("/{brand_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_brand(
    brand_id: int,
    service: FromDishka[BrandService],
):
    deleted_brand = await service.delete_brand(brand_id)
    if deleted_brand is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand not found",
        )
