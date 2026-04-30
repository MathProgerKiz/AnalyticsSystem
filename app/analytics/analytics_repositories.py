import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import Select, func, select

from app.models.order import Order, OrderItem
from app.models.product import BrandFeature, Product, ProductType


class AnalyticsRepository:
    def __init__(self, db):
        self.db = db

    def _period_filter(
        self,
        stmt: Select,
        start_date: datetime.datetime | None,
        end_date: datetime.datetime | None,
    ) -> Select:
        if start_date is not None:
            stmt = stmt.where(Order.create_date >= start_date)
        if end_date is not None:
            stmt = stmt.where(Order.create_date <= end_date)
        return stmt

    async def _execute_mappings(self, stmt: Select) -> list[dict[str, Any]]:
        result = await self.db.execute(stmt)
        return [dict(row) for row in result.mappings().all()]

    async def get_sales_summary(
        self,
        start_date: datetime.datetime | None = None,
        end_date: datetime.datetime | None = None,
    ) -> dict[str, Decimal | int | None]:
        stmt = select(
            func.count(Order.id).label("orders_count"),
            func.coalesce(func.sum(Order.total_price), 0).label("total_revenue"),
            func.coalesce(func.avg(Order.total_price), 0).label("average_order_value"),
        ).select_from(Order)
        stmt = self._period_filter(stmt, start_date, end_date)

        result = await self.db.execute(stmt)
        row = result.mappings().one()
        return dict(row)

    async def get_top_selling_products(self, limit: int = 10) -> list[dict[str, Any]]:
        stmt = (
            select(
                Product.id.label("product_id"),
                Product.name.label("product_name"),
                func.sum(OrderItem.quantity).label("total_quantity"),
                func.sum(OrderItem.quantity * Product.price).label("total_revenue"),
            )
            .select_from(OrderItem)
            .join(Product, OrderItem.product_id == Product.id)
            .group_by(Product.id, Product.name)
            .order_by(func.sum(OrderItem.quantity).desc())
            .limit(max(limit, 1))
        )
        return await self._execute_mappings(stmt)

    async def get_sales_by_period(
        self,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
    ) -> list[dict[str, Any]]:
        stmt = (
            select(
                Product.id.label("product_id"),
                Product.name.label("product_name"),
                func.sum(OrderItem.quantity).label("total_quantity"),
                func.sum(OrderItem.quantity * Product.price).label("total_revenue"),
            )
            .select_from(Order)
            .join(OrderItem, Order.id == OrderItem.order_id)
            .join(Product, OrderItem.product_id == Product.id)
            .where(Order.create_date.between(start_date, end_date))
            .group_by(Product.id, Product.name)
            .order_by(func.sum(OrderItem.quantity * Product.price).desc())
        )
        return await self._execute_mappings(stmt)

    async def get_top_sales_by_period(
        self,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        stmt = (
            select(
                Product.id.label("product_id"),
                Product.name.label("product_name"),
                func.sum(OrderItem.quantity).label("total_quantity"),
                func.sum(OrderItem.quantity * Product.price).label("total_revenue"),
            )
            .select_from(Order)
            .join(OrderItem, Order.id == OrderItem.order_id)
            .join(Product, OrderItem.product_id == Product.id)
            .where(Order.create_date.between(start_date, end_date))
            .group_by(Product.id, Product.name)
            .order_by(func.sum(OrderItem.quantity * Product.price).desc())
            .limit(max(limit, 1))
        )
        return await self._execute_mappings(stmt)

    async def get_top_selling_products_by_brand(
        self,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        stmt = (
            select(
                BrandFeature.id.label("brand_id"),
                BrandFeature.brand_name.label("brand"),
                func.sum(OrderItem.quantity).label("total_quantity"),
                func.sum(OrderItem.quantity * Product.price).label("total_revenue"),
            )
            .select_from(OrderItem)
            .join(Product, OrderItem.product_id == Product.id)
            .join(BrandFeature, Product.brand_id == BrandFeature.id)
            .group_by(BrandFeature.id, BrandFeature.brand_name)
            .order_by(func.sum(OrderItem.quantity).desc())
            .limit(max(limit, 1))
        )
        return await self._execute_mappings(stmt)

    async def get_top_selling_products_by_type(
        self,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        stmt = (
            select(
                ProductType.id.label("product_type_id"),
                ProductType.product_type.label("type"),
                func.sum(OrderItem.quantity).label("total_quantity"),
                func.sum(OrderItem.quantity * Product.price).label("total_revenue"),
            )
            .select_from(OrderItem)
            .join(Product, OrderItem.product_id == Product.id)
            .join(ProductType, Product.product_type_id == ProductType.id)
            .group_by(ProductType.id, ProductType.product_type)
            .order_by(func.sum(OrderItem.quantity).desc())
            .limit(max(limit, 1))
        )
        return await self._execute_mappings(stmt)

    async def get_sales_brand_by_period(
        self,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
    ) -> list[dict[str, Any]]:
        stmt = (
            select(
                BrandFeature.id.label("brand_id"),
                BrandFeature.brand_name.label("brand"),
                func.sum(OrderItem.quantity).label("total_quantity"),
                func.sum(OrderItem.quantity * Product.price).label("total_revenue"),
            )
            .select_from(Order)
            .join(OrderItem, Order.id == OrderItem.order_id)
            .join(Product, OrderItem.product_id == Product.id)
            .join(BrandFeature, Product.brand_id == BrandFeature.id)
            .where(Order.create_date.between(start_date, end_date))
            .group_by(BrandFeature.id, BrandFeature.brand_name)
            .order_by(func.sum(OrderItem.quantity * Product.price).desc())
        )
        return await self._execute_mappings(stmt)

    async def get_sales_type_by_period(
        self,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
    ) -> list[dict[str, Any]]:
        stmt = (
            select(
                ProductType.id.label("product_type_id"),
                ProductType.product_type.label("type"),
                func.sum(OrderItem.quantity).label("total_quantity"),
                func.sum(OrderItem.quantity * Product.price).label("total_revenue"),
            )
            .select_from(Order)
            .join(OrderItem, Order.id == OrderItem.order_id)
            .join(Product, OrderItem.product_id == Product.id)
            .join(ProductType, Product.product_type_id == ProductType.id)
            .where(Order.create_date.between(start_date, end_date))
            .group_by(ProductType.id, ProductType.product_type)
            .order_by(func.sum(OrderItem.quantity * Product.price).desc())
        )
        return await self._execute_mappings(stmt)

    async def get_sales_dynamics_by_day(
        self,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
    ) -> list[dict[str, Any]]:
        day = func.date(Order.create_date)
        return await self._get_sales_dynamics(day, start_date, end_date)

    async def get_sales_dynamics_by_week(
        self,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
    ) -> list[dict[str, Any]]:
        week = func.strftime("%Y-%W", Order.create_date)
        return await self._get_sales_dynamics(week, start_date, end_date)

    async def get_sales_dynamics_by_month(
        self,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
    ) -> list[dict[str, Any]]:
        month = func.strftime("%Y-%m", Order.create_date)
        return await self._get_sales_dynamics(month, start_date, end_date)

    async def _get_sales_dynamics(
        self,
        period_expression,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
    ) -> list[dict[str, Any]]:
        stmt = (
            select(
                period_expression.label("period"),
                func.count(func.distinct(Order.id)).label("orders_count"),
                func.sum(OrderItem.quantity).label("total_quantity"),
                func.sum(OrderItem.quantity * Product.price).label("total_revenue"),
            )
            .select_from(Order)
            .join(OrderItem, Order.id == OrderItem.order_id)
            .join(Product, OrderItem.product_id == Product.id)
            .where(Order.create_date.between(start_date, end_date))
            .group_by(period_expression)
            .order_by(period_expression)
        )
        return await self._execute_mappings(stmt)


AnalicsRepository = AnalyticsRepository
