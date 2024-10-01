import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, UUID, Boolean, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from ..base_schema import BaseSchemaUserItem


class UserMarketSchema(BaseSchemaUserItem):
    __tablename__ = "tb_user_market"
    __table_args__ = (
        UniqueConstraint(
            "cd_user", "preference", name="unique_preference_per_user", deferrable=True, initially="DEFERRED"
        ),
        UniqueConstraint("name", "cd_user", name="unique_market_per_user"),
        {"schema": "user"},
    )

    id_user_market: Mapped[uuid.UUID] = mapped_column(UUID(), primary_key=True, default_factory=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(length=50), nullable=False, unique=True)
    preference: Mapped[bool] = mapped_column(Boolean(), default=False, nullable=False)
    last_update: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    creation: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
