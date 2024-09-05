from datetime import date

from sqlalchemy import String, Date, Enum, Boolean
from sqlalchemy.orm import Mapped, MappedColumn

from app.DataBase.schemas.base_schemas import BaseSchema
from app.Enums.enums import LangEnum


class User(BaseSchema):
    __tablename__ = "user"

    email: Mapped[str] = MappedColumn(String(length=255), unique=True, nullable=False)
    password: Mapped[str] = MappedColumn(String(length=80), nullable=False)
    language: Mapped[LangEnum] = MappedColumn(Enum(LangEnum), nullable=False)
    birthdate: Mapped[date] = MappedColumn(Date, nullable=False)
    is_active: Mapped[bool] = MappedColumn(Boolean, default=True)

    def __repr__(self) -> str:
        return f"Nome: {self.name}, Email: {self.email}"
