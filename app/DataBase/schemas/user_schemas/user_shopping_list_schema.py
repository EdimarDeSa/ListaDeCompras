import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, UUID, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from ..base_schema import BaseSchemaUserItem


class UserShoppingListSchema(BaseSchemaUserItem):
    __tablename__ = "tb_user_shopping_list"
    __table_args__ = (
        {"schema": "user"},
        UniqueConstraint("name", "cd_user", name="unique_shopping_list_per_user"),
    )

    id_user_shopping_list: Mapped[uuid.UUID] = mapped_column(UUID(), primary_key=True, default_factory=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    final_value: Mapped[int] = mapped_column(Integer, default=0)
    unique_itens: Mapped[int] = mapped_column(Integer, default=0)
    total_itens: Mapped[int] = mapped_column(Integer, default=0)
    last_update: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    creation: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
