from datetime import date

from sqlalchemy import String, Date, Enum, Boolean
from sqlalchemy.orm import Mapped, MappedColumn, relationship

from DataBase.schemas.base_schemas import BaseSchema
from Enums.enums import LangEnum


class User(BaseSchema):
    __tablename__ = "user"

    email: Mapped[str] = MappedColumn(String(length=255), unique=True, nullable=False)
    password: Mapped[str] = MappedColumn(String(length=80), nullable=False)
    language: Mapped[LangEnum] = MappedColumn(Enum(LangEnum), nullable=False)
    birthdate: Mapped[date] = MappedColumn(Date, nullable=False)
    is_active: Mapped[bool] = MappedColumn(Boolean, default=True)

    products: Mapped[list["UserProduct"]] = relationship(
        "UserProduct",
        order_by="UserProduct.name",
        viewonly=True,
        back_populates="user",
        cascade="all, delete-orphan",
    )
    categories: Mapped[list["UserCategory"]] = relationship(
        "UserCategory",
        back_populates="user",
        cascade="all, delete-orphan",
        order_by="UserCategory.name",
    )
