import uuid
from datetime import date, datetime

from sqlalchemy import TIMESTAMP, UUID, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from ..base_schema import BaseSchemaUserItem


class UserShoppingLogSchema(BaseSchemaUserItem):
    __tablename__ = "tb_user_shopping_log"
    __table_args__ = (
        {"schema": "user"},
        UniqueConstraint(
            "cd_user", "cd_user_shopping_list", "cd_user_market", name="unique_shopping_log_per_user_per_market"
        ),
    )

    id_user_shopping_log: Mapped[uuid.UUID] = mapped_column(UUID(), primary_key=True, default_factory=uuid.uuid4)
    shopping_date: Mapped[date] = mapped_column(DateTime, nullable=False, default_factory=date.today)
    cd_user_shopping_list: Mapped[uuid.UUID] = mapped_column(
        UUID(), ForeignKey("user.tb_user_shopping_list.id_user_shopping_list"), nullable=False
    )
    cd_user_market: Mapped[uuid.UUID] = mapped_column(
        UUID(), ForeignKey("user.tb_user_market.id_user_market"), nullable=False
    )
    last_update: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    creation: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)

    def __str__(self):
        return f"{self.market_id.name} - {self.shopping_list_id.name}"
