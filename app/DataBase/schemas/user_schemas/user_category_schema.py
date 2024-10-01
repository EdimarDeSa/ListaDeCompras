import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, UUID, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from ..base_schema import BaseSchemaUserItem


class UserCategorySchema(BaseSchemaUserItem):
    __tablename__ = "tb_user_category"
    __table_args__ = (
        {"schema": "user"},
        UniqueConstraint("name", "cd_user", name="unique_category_per_user"),
    )

    id_user_category: Mapped[uuid.UUID] = mapped_column(UUID(), primary_key=True, default_factory=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(length=100), nullable=False)
    last_update: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    creation: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
