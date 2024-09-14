from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, MappedColumn, relationship

from DataBase.schemas.base_schemas import BaseSchema


class UnityType(BaseSchema):
    __tablename__ = "unity_type"

    name: Mapped[str] = MappedColumn(String(length=100), nullable=False, unique=True)
    base_calc: Mapped[int] = MappedColumn(Integer)
    abbreviation: Mapped[str] = MappedColumn(String(5), nullable=False, unique=True)

    default_products: Mapped[list["DefaultProduct"]] = relationship("DefaultProduct", back_populates="unity_type")
