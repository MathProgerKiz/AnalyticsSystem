from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.order import Order, OrderItem
from app.models.product import Product


class OrderRepository:
    def __init__(self, db):
        self.db = db

    async def _calculate_total_price(self, items_data):
        if not items_data:
            raise ValueError("Order must contain at least one item")

        product_ids = {item["product_id"] for item in items_data}
        result = await self.db.scalars(
            select(Product).where(Product.id.in_(product_ids))
        )
        products = {product.id: product for product in result.all()}

        missing_product_ids = product_ids - set(products)
        if missing_product_ids:
            missing_ids = ", ".join(
                str(product_id) for product_id in missing_product_ids
            )
            raise ValueError(f"Products not found: {missing_ids}")

        return sum(
            products[item["product_id"]].price * item["quantity"] for item in items_data
        )

    async def create_order(self, order_data):
        items_data = order_data["items"]
        total_price = await self._calculate_total_price(items_data)
        order = Order(total_price=total_price)
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
        order = await self.get_order(order_id)
        if order is None:
            return None
        if "items" in order_data:
            order.total_price = await self._calculate_total_price(items_data)
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
