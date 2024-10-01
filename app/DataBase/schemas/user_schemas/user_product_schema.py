import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, UUID, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base_schema import BaseSchemaUserItem


class UserProductSchema(BaseSchemaUserItem):
    __tablename__ = "tb_user_product"
    __table_args__ = (
        {"schema": "user"},
        UniqueConstraint("name", "cd_user", name="unique_product_per_user"),
    )

    id_user_product: Mapped[uuid.UUID] = mapped_column(UUID(), primary_key=True, default_factory=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    cd_user_unit_type: Mapped[uuid.UUID] = mapped_column(
        UUID(), ForeignKey("user.tb_user_unit_type.id_user_unit_type"), nullable=False
    )
    price: Mapped[int] = mapped_column(Integer(), default=0, nullable=False)
    cd_price_unit_type: Mapped[uuid.UUID] = mapped_column(
        UUID(), ForeignKey("user.tb_user_unit_type.id_user_unit_type"), nullable=False
    )
    cd_user_category: Mapped[uuid.UUID] = mapped_column(
        UUID(), ForeignKey("user.tb_user_category.id_user_category"), nullable=False
    )
    notes: Mapped[str] = mapped_column(Text(), nullable=True, default=None)
    barcode: Mapped[str] = mapped_column(String(50), nullable=True, default=None)
    image_url: Mapped[str] = mapped_column(Text(), nullable=True, default=None)
    last_update: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    creation: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
