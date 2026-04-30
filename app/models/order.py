
import datetime
from decimal import Decimal
from typing import List

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Integer, Text

from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Product


class OrderItem(Base):
    __tablename__ = 'order_item'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(
        ForeignKey('orders.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(
        ForeignKey('product.id'), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    order: Mapped['Order'] = relationship(back_populates='items')
    product: Mapped['Product'] = relationship(back_populates='order_items')


class Order(Base):
    __tablename__ = 'orders'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    total_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False)

    items: Mapped[List['OrderItem']] = relationship(back_populates='order')
    create_date: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow)
