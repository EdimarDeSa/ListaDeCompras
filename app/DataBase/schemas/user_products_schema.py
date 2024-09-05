from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint, UUID, Text
from sqlalchemy.orm import MappedColumn

from app.DataBase.schemas.base_schema import BaseSchemaUserProperty


class UserProducts(BaseSchemaUserProperty):
    __tablename__ = "user_products"

    unity_types_id = MappedColumn(UUID, ForeignKey("unity_type.id"), nullable=False)
    price = MappedColumn(Integer, default=0)
    price_unity_types_id = MappedColumn(ForeignKey("unity_type.id"), nullable=False)
    category_id = MappedColumn(ForeignKey("user_categorys.id"), nullable=False)
    notes = MappedColumn(String(255), nullable=True)
    barcode = MappedColumn(String(50), nullable=True)
    image_url = MappedColumn(Text, nullable=True)

    __table_args__ = (UniqueConstraint("name", "user_id"),)
