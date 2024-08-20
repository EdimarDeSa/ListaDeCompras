import uuid
from datetime import date, datetime

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, registry

from app.Enums.enums import LangEnum
from app.Utils.utils import datetime_now_utc

reg = registry()


class Base(DeclarativeBase):
    __abstract__ = True
    registry = reg


class DeclarativeBaseModel(Base):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(sa.UUID, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(sa.String(length=100), nullable=False)
    creation: Mapped[datetime] = mapped_column(sa.DateTime, default=datetime_now_utc, nullable=False)
    last_update: Mapped[datetime] = mapped_column(
        sa.DateTime,
        default=datetime_now_utc,
        nullable=False,
        onupdate=datetime_now_utc,
    )

    def __repr__(self) -> str:
        return f"<{self.__name__}.name = {self.name}>"

    def __str__(self) -> str:
        return self.name


class User(DeclarativeBaseModel):
    __tablename__ = "user"

    email: Mapped[str] = mapped_column(sa.String(length=255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(sa.String(length=80), nullable=False)
    language: Mapped[LangEnum] = mapped_column(sa.Enum(LangEnum), nullable=False)
    birthdate: Mapped[date] = mapped_column(sa.Date, nullable=False)

    def __repr__(self) -> str:
        return f"Nome: {self.name}, Email: {self.email}"


class DefaultCategory(DeclarativeBaseModel):
    __tablename__ = "default_category"
    name: Mapped[str] = mapped_column(sa.String(length=100), nullable=False, unique=True)


class UnityType(DeclarativeBaseModel):
    __tablename__ = "unity_type"

    name: Mapped[str] = mapped_column(sa.String(length=100), nullable=False, unique=True)
    base_calc: Mapped[int] = mapped_column(sa.Integer)
    abbreviation: Mapped[str] = mapped_column(sa.String(5), nullable=False, unique=True)


class DefaultProduct(DeclarativeBaseModel):
    __tablename__ = "default_products"

    unit_type_id: Mapped[uuid.UUID] = mapped_column(sa.ForeignKey("unity_type.id"), nullable=False)
    category_id: Mapped[uuid.UUID] = mapped_column(sa.ForeignKey("default_category.id"), nullable=False)
    image_url: Mapped[str] = mapped_column(sa.Text)
