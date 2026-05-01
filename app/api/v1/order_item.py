from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, HTTPException, status

from app.schemas.order_item import (
    OrderItemCreate,
    OrderItemRead,
    OrderItemUpdate,
)
from app.services.order_item import OrderItemService


router = APIRouter(
    prefix="/order-items",
    tags=["order items"],
)


@router.post("/", response_model=OrderItemRead, status_code=status.HTTP_201_CREATED)
@inject
async def create_order_item(
    order_item: OrderItemCreate,
    service: FromDishka[OrderItemService],
):
    return await service.create_order_item(order_item.model_dump())


@router.get("/", response_model=list[OrderItemRead])
@inject
async def get_order_items(
    service: FromDishka[OrderItemService],
):
    return await service.get_order_items()


@router.get("/by-order/{order_id}", response_model=list[OrderItemRead])
@inject
async def get_order_items_by_order(
    order_id: int,
    service: FromDishka[OrderItemService],
):
    return await service.get_order_items_by_order(order_id)


@router.get("/{order_item_id}", response_model=OrderItemRead)
@inject
async def get_order_item(
    order_item_id: int,
    service: FromDishka[OrderItemService],
):
    order_item = await service.get_order_item(order_item_id)
    if order_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order item not found",
        )
    return order_item


@router.patch("/{order_item_id}", response_model=OrderItemRead)
@inject
async def update_order_item(
    order_item_id: int,
    order_item: OrderItemUpdate,
    service: FromDishka[OrderItemService],
):
    updated_order_item = await service.update_order_item(
        order_item_id,
        order_item.model_dump(exclude_unset=True),
    )
    if updated_order_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order item not found",
        )
    return updated_order_item


@router.delete("/{order_item_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_order_item(
    order_item_id: int,
    service: FromDishka[OrderItemService],
):
    deleted_order_item = await service.delete_order_item(order_item_id)
    if deleted_order_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order item not found",
        )
