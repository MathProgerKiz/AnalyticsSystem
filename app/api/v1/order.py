from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, HTTPException, status

from app.schemas.order import OrderCreate, OrderRead, OrderUpdate
from app.services.order import OrderService


router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)


@router.post("/", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
@inject
async def create_order(
    order: OrderCreate,
    service: FromDishka[OrderService],
):
    try:
        return await service.create_order(order.model_dump())
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.get("/", response_model=list[OrderRead])
@inject
async def get_orders(
    service: FromDishka[OrderService],
):
    return await service.get_orders()


@router.get("/{order_id}", response_model=OrderRead)
@inject
async def get_order(
    order_id: int,
    service: FromDishka[OrderService],
):
    order = await service.get_order(order_id)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    return order


@router.patch("/{order_id}", response_model=OrderRead)
@inject
async def update_order(
    order_id: int,
    order: OrderUpdate,
    service: FromDishka[OrderService],
):
    try:
        updated_order = await service.update_order(
            order_id,
            order.model_dump(exclude_unset=True),
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    if updated_order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    return updated_order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_order(
    order_id: int,
    service: FromDishka[OrderService],
):
    deleted_order = await service.delete_order(order_id)
    if deleted_order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
