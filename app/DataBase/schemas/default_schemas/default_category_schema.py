import uuid

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..base_schema import BaseSchema


class DefaultCategorySchema(BaseSchema):
    __tablename__ = "tb_default_category"
    __table_args__ = {"schema": "default"}

    id_default_category: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(length=50), nullable=False, unique=True)
