import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, UUID, Boolean, Float, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from ..base_schema import BaseSchema


class ProductListSchema(BaseSchema):
    __tablename__ = "tb_product_list"
    __table_args__ = (
        {"schema": "user"},
        UniqueConstraint("cd_user_shopping_list", "cd_user_product", name="unique_product_list_per_shopping_list"),
    )

    id_product_list: Mapped[uuid.UUID] = mapped_column(UUID(), primary_key=True, default_factory=uuid.uuid4)
    cd_user_shopping_list: Mapped[uuid.UUID] = mapped_column(
        UUID(), ForeignKey("user.tb_user_shopping_list.id_user_shopping_list", ondelete="SET NULL"), nullable=False
    )
    cd_user_product: Mapped[uuid.UUID] = mapped_column(
        UUID(), ForeignKey("user.tb_user_product.id_user_product", ondelete="SET NULL"), nullable=False
    )
    quantity: Mapped[int] = mapped_column(Integer(), default=1)
    price: Mapped[float] = mapped_column(Float(precision=2), default=0)
    total: Mapped[float] = mapped_column(Float(precision=2), default=0)
    on_cart: Mapped[bool] = mapped_column(Boolean(), default=False)
    last_update: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    creation: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
