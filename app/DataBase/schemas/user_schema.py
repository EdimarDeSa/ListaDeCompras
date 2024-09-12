from datetime import date

from sqlalchemy import String, Date, Enum, Boolean
from sqlalchemy.orm import Mapped, MappedColumn, relationship

from DataBase.schemas.base_schemas import BaseSchema
from DataBase.schemas.user_categories_schema import UserCategories
from DataBase.schemas.user_products_schema import UserProducts
from Enums.enums import LangEnum


class TbUser(BaseSchema):
    __tablename__ = "user"

    email: Mapped[str] = MappedColumn(String(length=255), unique=True, nullable=False)
    password: Mapped[str] = MappedColumn(String(length=80), nullable=False)
    language: Mapped[LangEnum] = MappedColumn(Enum(LangEnum), nullable=False)
    birthdate: Mapped[date] = MappedColumn(Date, nullable=False)
    is_active: Mapped[bool] = MappedColumn(Boolean, default=True)

    products: Mapped[list["UserProducts"]] = relationship(
        "UserProducts",
        order_by=UserProducts.name,
        viewonly=True,
        backref="user",
        cascade="all, delete-orphan",
    )
    categories: Mapped[list["UserCategories"]] = relationship(
        "UserCategories", backref="user", cascade="all, delete-orphan", order_by=UserCategories.name
    )
