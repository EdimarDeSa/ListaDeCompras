from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint, UUID, Text
from sqlalchemy.orm import MappedColumn

from DataBase.schemas.base_schemas import BaseSchemaUserProperty


class UserProducts(BaseSchemaUserProperty):
    __tablename__ = "user_product"
    __table_args__ = (UniqueConstraint("name", "user_id"),)

    unity_types_id = MappedColumn(UUID, ForeignKey("unity_type.id"), nullable=False)
    price = MappedColumn(Integer, default=0, nullable=False)
    price_unity_types_id = MappedColumn(ForeignKey("unity_type.id"), nullable=False)
    category_id = MappedColumn(ForeignKey("user_category.id"), nullable=False)
    notes = MappedColumn(String(255), nullable=True, default=None)
    barcode = MappedColumn(String(50), nullable=True, default=None)
    image_url = MappedColumn(Text, nullable=True, default=None)
