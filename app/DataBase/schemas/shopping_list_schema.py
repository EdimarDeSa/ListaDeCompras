from sqlalchemy import Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, MappedColumn

from app.DataBase.schemas.base_schema import BaseSchemaUserProperty


class ShoppingList(BaseSchemaUserProperty):
    __tablename__ = "shopping_list"

    final_value: Mapped[int] = MappedColumn(Integer, default=0)
    unique_items: Mapped[int] = MappedColumn(Integer, default=0)
    total_items: Mapped[int] = MappedColumn(Integer, default=0)

    __table_args__ = (UniqueConstraint("name", "user_id"),)
