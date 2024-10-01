import uuid
from datetime import datetime

from sqlalchemy import JSON, TIMESTAMP, UUID, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from ..base_schema import BaseSchema


class AdminEventSchema(BaseSchema):
    __tablename__ = "admin_event"
    __table_args__ = {"schema": "admin"}

    id_admin_event: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement="auto")
    cd_admin: Mapped[uuid.UUID] = mapped_column(
        UUID(), ForeignKey("admin.tb_admin.id_admin", ondelete="SET NULL"), nullable=False
    )
    cd_admin_event_type: Mapped[int] = mapped_column(
        Integer(), ForeignKey("admin.tb_admin_event_type.id_admin_event_type", ondelete="SET NULL"), nullable=False
    )
    comment: Mapped[JSON] = mapped_column(JSON(none_as_null=True), default_factory=dict, nullable=True)
    creation: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
