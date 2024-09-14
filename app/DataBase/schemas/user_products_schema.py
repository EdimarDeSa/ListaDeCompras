import uuid

from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint, UUID, Text
from sqlalchemy.orm import MappedColumn, relationship, Mapped

from DataBase.schemas.base_schemas import BaseSchemaUserProperty


class UserProduct(BaseSchemaUserProperty):
    __tablename__ = "user_product"
    __table_args__ = (UniqueConstraint("name", "user_id"),)
    unity_types_id: Mapped[uuid.UUID] = MappedColumn(UUID, ForeignKey("unity_type.id"), nullable=False)
    price: Mapped[int] = MappedColumn(Integer, default=0, nullable=False)
    price_unity_types_id: Mapped[uuid.UUID] = MappedColumn(ForeignKey("unity_type.id"), nullable=False)
    category_id: Mapped[uuid.UUID] = MappedColumn(ForeignKey("user_category.id"), nullable=False)
    notes: Mapped[str] = MappedColumn(String(255), nullable=True, default=None)
    barcode: Mapped[str] = MappedColumn(String(50), nullable=True, default=None)
    image_url: Mapped[str] = MappedColumn(Text, nullable=True, default=None)

    user: Mapped[list["User"]] = relationship(
        "User",
        viewonly=True,
        back_populates="products",
    )
