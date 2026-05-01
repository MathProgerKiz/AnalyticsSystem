from decimal import Decimal
from typing import List

from sqlalchemy import ForeignKey, Numeric, String, Integer, Text

from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class BrandFeature(Base):
    __tablename__ = "brandfeature"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    brand_name: Mapped[str] = mapped_column(String(32), nullable=False)

    products: Mapped[List["Product"]] = relationship(back_populates="brand")


class ProductType(Base):
    __tablename__ = "product_type"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_type: Mapped[str] = mapped_column(String(32), nullable=False)

    products: Mapped[List["Product"]] = relationship(back_populates="product_type")


class Product(Base):
    __tablename__ = "product"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    brand_id: Mapped[int] = mapped_column(ForeignKey("brandfeature.id"), nullable=False)
    product_type_id: Mapped[int] = mapped_column(
        ForeignKey("product_type.id"), nullable=False
    )

    brand: Mapped["BrandFeature"] = relationship(
        back_populates="products", lazy="selectin"
    )
    product_type: Mapped["ProductType"] = relationship(
        back_populates="products", lazy="selectin"
    )
