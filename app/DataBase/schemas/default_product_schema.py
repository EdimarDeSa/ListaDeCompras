import uuid

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, MappedColumn

from app.DataBase.schemas.base_schemas import BaseSchema


class DefaultProduct(BaseSchema):
    __tablename__ = "default_products"

    unit_type_id: Mapped[uuid.UUID] = MappedColumn(ForeignKey("unity_type.id"), nullable=False)
    default_category_id: Mapped[uuid.UUID] = MappedColumn(ForeignKey("default_category.id"), nullable=False)
    image_url: Mapped[str] = MappedColumn(Text)
