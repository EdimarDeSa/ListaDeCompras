from sqlalchemy import String
from sqlalchemy.orm import Mapped, MappedColumn

from app.DataBase.schemas.base_schemas import BaseSchema


class DefaultCategory(BaseSchema):
    __tablename__ = "default_category"
    name: Mapped[str] = MappedColumn(String(length=100), nullable=False, unique=True)
