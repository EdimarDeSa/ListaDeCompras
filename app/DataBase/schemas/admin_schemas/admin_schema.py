import uuid
from datetime import date, datetime

from sqlalchemy import TIMESTAMP, UUID, Boolean, Date, String
from sqlalchemy.orm import Mapped, mapped_column

from ..base_schema import BaseSchema


class AdminSchema(BaseSchema):
    __tablename__ = "tb_admin"
    __table_args__ = {"schema": "admin"}

    id_admin: Mapped[uuid.UUID] = mapped_column(UUID(), primary_key=True, default_factory=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    birthdate: Mapped[date] = mapped_column(Date(), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True, nullable=False)
    last_update: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    creation: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
