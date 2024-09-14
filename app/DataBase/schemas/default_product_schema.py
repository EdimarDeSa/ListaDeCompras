import uuid

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, MappedColumn, relationship

from DataBase.schemas.base_schemas import BaseSchema
from DataBase.schemas.default_category_schema import DefaultCategory
from DataBase.schemas.unity_type_schema import UnityType


class DefaultProduct(BaseSchema):
    __tablename__ = "default_products"

    unit_type_id: Mapped[uuid.UUID] = MappedColumn(ForeignKey("unity_type.id"), nullable=False)
    default_category_id: Mapped[uuid.UUID] = MappedColumn(ForeignKey("default_category.id"), nullable=False)
    image_url: Mapped[str] = MappedColumn(Text)

    unity_type: Mapped["UnityType"] = relationship("UnityType", back_populates="default_products")
    default_category: Mapped["DefaultCategory"] = relationship("UnityType", back_populates="default_products")
