

import datetime

from sqlalchemy import func, select

from app.models.order import Order, OrderItem
from app.models import Product


class AnalicsRepository:
    def __init__(self, db):
        self.db = db
    
    async def get_top_selling_products(self, limit: int = 10):
        stmt = (select(
            Product.name,
            func.count(OrderItem.id).label('total_sold')
        )
        .join(OrderItem, Order.id == OrderItem.order_id)
        .join(Product, OrderItem.product_id == Product.id)
        .group_by(Product.id).order_by(func.count(OrderItem.id).desc())
        .limit(limit))
        result = await self.db.execute(stmt)
        return result.all() 
    
    async def get_sales_by_period(self, start_date: datetime, end_date: datetime):
       
        stmt = (select(
            Product.name,
            func.sum(OrderItem.quantity).label('total_quantity'),
            func.sum(OrderItem.quantity * Product.price).label('total_revenue')
        )
        .join(OrderItem, Order.id == OrderItem.order_id)
        .join(Product, OrderItem.product_id == Product.id)
        .where(Order.create_date.between(start_date, end_date))
        .group_by(Product.id))
        result = await self.db.scalars(stmt)
        return result.all()
    
    async def get_top_sales_by_period(self, start_date: datetime, end_date: datetime, limit: int = 10):
        stmt = (select(
            Product.name,
            func.sum(OrderItem.quantity).label('total_quantity'),
            func.sum(OrderItem.quantity * Product.price).label('total_revenue')
        )
        .join(OrderItem, Order.id == OrderItem.order_id)
        .join(Product, OrderItem.product_id == Product.id)
        .where(Order.create_date.between(start_date, end_date))
        .group_by(Product.id)
        .order_by(func.sum(OrderItem.quantity * Product.price).desc())
        .limit(limit))
        result = await self.db.scalars(stmt)
        return result.all()
    
    async def get_top_selling_products_by_brand(self, limit: int = 10):
        stmt = (select(
            Product.brand_name.label('brand'),
            func.count(OrderItem.id).label('total_sold')
        )
        .join(OrderItem, Order.id == OrderItem.order_id)
        .join(Product, OrderItem.product_id == Product.id)
        .group_by(Product.brand_name)
        .order_by(func.count(OrderItem.id).desc())
        .limit(limit))
        result = await self.db.scalars(stmt)
        return result.all()
    
    async def get_top_selling_products_by_type(self, limit: int = 10):
        stmt = (select(
            Product.product_type.label('type'),
            func.count(OrderItem.id).label('total_sold')
        )
        .join(OrderItem, Order.id == OrderItem.order_id)
        .join(Product, OrderItem.product_id == Product.id)
        .group_by(Product.product_type)
        .order_by(func.count(OrderItem.id).desc())
        .limit(limit))
        result = await self.db.scalars(stmt)
        return result.all()
    
    async def get_sales_brand_by_period(self, start_date: datetime, end_date: datetime):
        stmt = (select(
            Product.brand_name.label('brand'),
            func.sum(OrderItem.quantity).label('total_quantity'),
            func.sum(OrderItem.quantity * Product.price).label('total_revenue')
        )
        .join(OrderItem, Order.id == OrderItem.order_id)
        .join(Product, OrderItem.product_id == Product.id)
        .where(Order.create_date.between(start_date, end_date))
        .group_by(Product.brand_name))
        result = await self.db.scalars(stmt)
        return result.all()
            
    async def get_sales_type_by_period(self, start_date: datetime, end_date: datetime):
        stmt = (select(
            Product.product_type.label('type'),
            func.sum(OrderItem.quantity).label('total_quantity'),
            func.sum(OrderItem.quantity * Product.price).label('total_revenue')
        )
        .join(OrderItem, Order.id == OrderItem.order_id)
        .join(Product, OrderItem.product_id == Product.id)
        .where(Order.create_date.between(start_date, end_date))
        .group_by(Product.product_type))
        result = await self.db.scalars(stmt)
        return result.all()
    
    
    
