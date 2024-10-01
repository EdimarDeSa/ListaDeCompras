from os import name

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from ..base_schema import BaseSchema


class DefaultProductSchema(BaseSchema):
    __tablename__ = "tb_default_product"
    __table_args__ = {"schema": "default"}

    id_default_products: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(length=100), nullable=False, unique=True)
    cd_unit_type: Mapped[int] = mapped_column(
        Integer(), ForeignKey("default.tb_default_unit_type.id_unit_type", ondelete="SET NULL"), nullable=False
    )
    default_category_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey("default.tb_default_category.id_default_category", ondelete="SET NULL"), nullable=False
    )
    image_url: Mapped[str] = mapped_column(Text(), nullable=True, default=None)
