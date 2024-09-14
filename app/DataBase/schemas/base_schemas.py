import uuid
from datetime import datetime

from sqlalchemy import String, ForeignKey, UUID, DateTime
from sqlalchemy.orm import Mapped, MappedColumn, DeclarativeBase, registry

from Utils.global_functions import datetime_now_utc

reg = registry()

reg.configure(cascade=True)


class BaseSchema(DeclarativeBase):
    __abstract__ = True
    registry = reg

    id: Mapped[uuid.UUID] = MappedColumn(UUID, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = MappedColumn(String(length=100), nullable=False, sort_order=True)
    creation: Mapped[datetime] = MappedColumn(DateTime, default=datetime_now_utc, nullable=False)
    last_update: Mapped[datetime] = MappedColumn(
        DateTime, default=datetime_now_utc, nullable=False, onupdate=datetime_now_utc
    )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}.id: {self.id}>"

    def __str__(self) -> str:
        return f"Name: {self.name}"


class BaseSchemaUserProperty(BaseSchema):
    __abstract__ = True

    name: Mapped[str] = MappedColumn(String(255), nullable=False, sort_order=True)
    user_id: Mapped[uuid.UUID] = MappedColumn(UUID, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
