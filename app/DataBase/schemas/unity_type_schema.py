from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, MappedColumn

from app.DataBase.schemas.base_schemas import BaseSchema


class UnityType(BaseSchema):
    __tablename__ = "unity_type"

    name: Mapped[str] = MappedColumn(String(length=100), nullable=False, unique=True)
    base_calc: Mapped[int] = MappedColumn(Integer)
    abbreviation: Mapped[str] = MappedColumn(String(5), nullable=False, unique=True)
