from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.order import OrderItem
from app.models.product import Product


class OrderItemRepository:
    def __init__(self, db):
        self.db = db

    async def create_order_item(self, order_item_data):
        order_item = OrderItem(**order_item_data)
        self.db.add(order_item)
        await self.db.commit()
        return await self.get_order_item(order_item.id)

    async def get_order_item(self, order_item_id):
        query = (
            select(OrderItem)
            .where(OrderItem.id == order_item_id)
            .options(
                selectinload(OrderItem.product).selectinload(Product.brand),
                selectinload(OrderItem.product).selectinload(Product.product_type),
            )
        )
        return await self.db.scalar(query)

    async def get_order_items(self):
        query = select(OrderItem).options(
            selectinload(OrderItem.product).selectinload(Product.brand),
            selectinload(OrderItem.product).selectinload(Product.product_type),
        )
        result = await self.db.scalars(query)
        return result.all()

    async def get_order_items_by_order(self, order_id):
        query = (
            select(OrderItem)
            .where(OrderItem.order_id == order_id)
            .options(
                selectinload(OrderItem.product).selectinload(Product.brand),
                selectinload(OrderItem.product).selectinload(Product.product_type),
            )
        )
        result = await self.db.scalars(query)
        return result.all()

    async def update_order_item(self, order_item_id, order_item_data):
        order_item = await self.get_order_item(order_item_id)
        if order_item is None:
            return None
        for key, value in order_item_data.items():
            setattr(order_item, key, value)
        await self.db.commit()
        return await self.get_order_item(order_item.id)

    async def delete_order_item(self, order_item_id):
        order_item = await self.get_order_item(order_item_id)
        if order_item is None:
            return None
        await self.db.delete(order_item)
        await self.db.commit()
        return order_item
