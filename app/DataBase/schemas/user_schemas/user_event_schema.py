from datetime import datetime

from sqlalchemy import JSON, TIMESTAMP, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from ..base_schema import BaseSchemaUserItem


class UserEventSchema(BaseSchemaUserItem):
    id_user_event: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement="auto")
    cd_user_event_type: Mapped[int] = mapped_column(
        Integer(), ForeignKey("user.tb_user_event_type.id_user_event_type"), nullable=False
    )
    comment: Mapped[JSON] = mapped_column(JSON(none_as_null=True), default_factory=dict, nullable=True)
    creation: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
