import uuid
from datetime import date

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, MappedColumn

from app.DataBase.schemas.base_schema import BaseSchemaUserProperty


class ShoppingLog(BaseSchemaUserProperty):
    __tablename__ = "shopping_log"

    shopping_list_id: Mapped[uuid.UUID] = MappedColumn(ForeignKey("shopping_list.id"), nullable=False)
    market_id: Mapped[uuid.UUID] = MappedColumn(ForeignKey("markets.id"), nullable=False)
    buy_date: Mapped[date] = MappedColumn(DateTime, nullable=False)

    def __str__(self):
        return f"{self.market_id.name} - {self.shopping_list_id.name}"
