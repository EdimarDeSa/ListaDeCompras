import uuid

from sqlalchemy import Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, MappedColumn

from DataBase.schemas.base_schemas import DeclarativeBase


class UserEvents(DeclarativeBase):
    __tablename__ = "user_events"

    id: Mapped[int] = MappedColumn(
        Integer,
        primary_key=True,
        default=uuid.uuid4,
        sort_order=True,
        autoincrement="auto",
    )
    description: Mapped[str] = MappedColumn(Text, nullable=False)
    user_id: Mapped[uuid.UUID] = MappedColumn(uuid.UUID, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
