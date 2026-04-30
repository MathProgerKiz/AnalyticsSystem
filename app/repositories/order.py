from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.order import Order, OrderItem
from app.models.product import Product


class OrderRepository:
    def __init__(self, db):
        self.db = db

    async def create_order(self, order_data):
        items_data = order_data.get("items", [])
        order_fields = {
            key: value for key, value in order_data.items() if key != "items"
        }
        order = Order(**order_fields)
        order.items = [OrderItem(**item_data) for item_data in items_data]
        self.db.add(order)
        await self.db.commit()
        return await self.get_order(order.id)

    async def get_order(self, order_id):
        query = (
            select(Order)
            .where(Order.id == order_id)
            .options(
                selectinload(Order.items)
                .selectinload(OrderItem.product)
                .selectinload(Product.brand),
                selectinload(Order.items)
                .selectinload(OrderItem.product)
                .selectinload(Product.product_type),
            )
        )
        return await self.db.scalar(query)

    async def get_orders(self):
        query = select(Order).options(
            selectinload(Order.items)
            .selectinload(OrderItem.product)
            .selectinload(Product.brand),
            selectinload(Order.items)
            .selectinload(OrderItem.product)
            .selectinload(Product.product_type),
        )
        result = await self.db.scalars(query)
        return result.all()

    async def get_all_orders(self):
        return await self.get_orders()

    async def update_order(self, order_id, order_data):
        items_data = order_data.get("items")
        order_fields = {
            key: value for key, value in order_data.items() if key != "items"
        }
        order = await self.get_order(order_id)
        if order is None:
            return None
        for key, value in order_fields.items():
            setattr(order, key, value)
        if "items" in order_data:
            order.items = [OrderItem(**item_data) for item_data in items_data]
        await self.db.commit()
        return await self.get_order(order.id)

    async def delete_order(self, order_id):
        order = await self.get_order(order_id)
        if order is None:
            return None
        await self.db.delete(order)
        await self.db.commit()
        return order
