import uuid
from datetime import date, datetime

from Enums.enums import LangEnum
from sqlalchemy import TIMESTAMP, UUID, Boolean, Date, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base_schema import BaseSchema


class UserSchema(BaseSchema):
    __tablename__ = "tb_user"
    __table_args__ = {"schema": "user"}

    id_user: Mapped[uuid.UUID] = mapped_column(UUID(), primary_key=True, default_factory=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(length=100), nullable=False)
    email: Mapped[str] = mapped_column(String(length=200), unique=True, nullable=False)
    birthdate: Mapped[date] = mapped_column(Date, nullable=False)
    language: Mapped[LangEnum] = mapped_column(String(6), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_update: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    creation: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)

    # products: Mapped[list["UserProduct"]] = relationship(
    #     "UserProduct",
    #     order_by="UserProduct.name",
    #     viewonly=True,
    #     back_populates="user",
    #     cascade="all, delete-orphan",
    # )
    # categories: Mapped[list["UserCategory"]] = relationship(
    #     "UserCategory",
    #     back_populates="user",
    #     cascade="all, delete-orphan",
    #     order_by="UserCategory.name",
    # )
