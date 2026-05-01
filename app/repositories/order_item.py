from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.models.order import Order, OrderItem
from app.models.product import Product


class OrderItemRepository:
    def __init__(self, db):
        self.db = db

    async def _recalculate_order_total_price(self, order_id):
        total_price = await self.db.scalar(
            select(func.coalesce(func.sum(OrderItem.quantity * Product.price), 0))
            .select_from(OrderItem)
            .join(Product, OrderItem.product_id == Product.id)
            .where(OrderItem.order_id == order_id)
        )
        order = await self.db.get(Order, order_id)
        if order is not None:
            order.total_price = total_price

    async def _validate_order_and_product(self, order_id, product_id):
        order = await self.db.get(Order, order_id)
        if order is None:
            raise ValueError(f"Order not found: {order_id}")

        product = await self.db.get(Product, product_id)
        if product is None:
            raise ValueError(f"Product not found: {product_id}")

    async def create_order_item(self, order_item_data):
        await self._validate_order_and_product(
            order_item_data["order_id"],
            order_item_data["product_id"],
        )
        order_item = OrderItem(**order_item_data)
        self.db.add(order_item)
        await self.db.flush()
        await self._recalculate_order_total_price(order_item.order_id)
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
        if "product_id" in order_item_data:
            await self._validate_order_and_product(
                order_item.order_id,
                order_item_data["product_id"],
            )
        for key, value in order_item_data.items():
            setattr(order_item, key, value)
        await self.db.flush()
        await self._recalculate_order_total_price(order_item.order_id)
        await self.db.commit()
        return await self.get_order_item(order_item.id)

    async def delete_order_item(self, order_item_id):
        order_item = await self.get_order_item(order_item_id)
        if order_item is None:
            return None
        order_id = order_item.order_id
        items_count = await self.db.scalar(
            select(func.count(OrderItem.id)).where(OrderItem.order_id == order_id)
        )
        if items_count <= 1:
            raise ValueError("Order must contain at least one item")
        await self.db.delete(order_item)
        await self.db.flush()
        await self._recalculate_order_total_price(order_id)
        await self.db.commit()
        return order_item
