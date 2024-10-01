from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base_schema import BaseSchema


class DefaultUnitTypeSchema(BaseSchema):
    __tablename__ = "tb_default_unit_type"
    __table_args__ = ({"schema": "default"},)

    id_unit_type: Mapped[int] = mapped_column(Integer(), nullable=False, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(length=100), nullable=False)
    abbreviation: Mapped[str] = mapped_column(String(10), nullable=False)
    base_calc: Mapped[int] = mapped_column(Integer(), nullable=False, default=1)
