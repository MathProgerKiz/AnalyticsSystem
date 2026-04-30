from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status

from app.schemas.brand import BrandCreate, BrandRead
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
