import uuid
from datetime import date

from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint, UUID, DateTime, Text, Boolean
from sqlalchemy.orm import Mapped, MappedColumn

from app.DataBase.schemas.base_schema import BaseSchema


class DefaultCategory(BaseSchema):
    __tablename__ = "default_category"
    name: Mapped[str] = MappedColumn(String(length=100), nullable=False, unique=True)


class UnityType(BaseSchema):
    __tablename__ = "unity_type"

    name: Mapped[str] = MappedColumn(String(length=100), nullable=False, unique=True)
    base_calc: Mapped[int] = MappedColumn(Integer)
    abbreviation: Mapped[str] = MappedColumn(String(5), nullable=False, unique=True)


class DefaultProduct(BaseSchema):
    __tablename__ = "default_products"

    unit_type_id: Mapped[uuid.UUID] = MappedColumn(ForeignKey("unity_type.id"), nullable=False)
    category_id: Mapped[uuid.UUID] = MappedColumn(ForeignKey("default_category.id"), nullable=False)
    image_url: Mapped[str] = MappedColumn(Text)


class Market(BaseSchemaUserProperty):
    __tablename__ = "market"

    __table_args__ = (UniqueConstraint("name", "user_id"),)


class UserCategorys(BaseSchemaUserProperty):
    __tablename__ = "user_categorys"

    __table_args__ = (UniqueConstraint("name", "user_id"),)


class UserProducts(BaseSchemaUserProperty):
    __tablename__ = "user_products"

    unity_types_id = MappedColumn(UUID, ForeignKey("unity_type.id"), nullable=False)
    price = MappedColumn(Integer, default=0)
    price_unity_types_id = MappedColumn(ForeignKey("unity_type.id"), nullable=False)
    category_id = MappedColumn(ForeignKey("user_categorys.id"), nullable=False)
    notes = MappedColumn(String(255), nullable=True)
    barcode = MappedColumn(String(50), nullable=True)
    image_url = MappedColumn(Text, nullable=True)

    __table_args__ = (UniqueConstraint("name", "user_id"),)


class ShoppingList(BaseSchemaUserProperty):
    __tablename__ = "shopping_list"

    final_value: Mapped[int] = MappedColumn(Integer, default=0)
    unique_items: Mapped[int] = MappedColumn(Integer, default=0)
    total_items: Mapped[int] = MappedColumn(Integer, default=0)

    __table_args__ = (UniqueConstraint("name", "user_id"),)


class ShoppingLog(BaseSchemaUserProperty):
    __tablename__ = "shopping_log"

    shopping_list_id: Mapped[uuid.UUID] = MappedColumn(ForeignKey("shopping_list.id"), nullable=False)
    market_id: Mapped[uuid.UUID] = MappedColumn(ForeignKey("markets.id"), nullable=False)
    buy_date: Mapped[date] = MappedColumn(DateTime, nullable=False)

    def __str__(self):
        return f"{self.market_id.name} - {self.shopping_list_id.name}"


class ProductList(BaseSchema):
    __tablename__ = "product_list"

    shopping_list_id = MappedColumn(Integer, ForeignKey("shopping_list.id"), nullable=False)
    user_product_id = MappedColumn(Integer, ForeignKey("user_products.id"), nullable=False)
    quantity = MappedColumn(Integer, default=1)
    price = MappedColumn(Integer, default=0)
    total = MappedColumn(Integer, default=0)
    on_cart = MappedColumn(Boolean, default=False)
