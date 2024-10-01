import uuid

from sqlalchemy import UUID, ForeignKey, String
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, registry

reg = registry()

reg.configure(cascade=True)

DeclarativeBase = declarative_base()


class BaseSchema(DeclarativeBase):
    __abstract__ = True
    registry = reg

    def __repr__(self) -> str:
        return f"{self.__tablename__}: {self.as_dict()}"

    def __str__(self) -> str:
        return f"Name: {self.name}"

    def as_dict(self, *, exclude_none: bool = False) -> dict:
        if exclude_none:
            return {c.name: getattr(self, c.name) for c in self.__table__.c if getattr(self, c.name) is not None}
        return {c.name: getattr(self, c.name) for c in self.__table__.c}


class BaseSchemaUserItem(BaseSchema):
    __abstract__ = True

    cd_user: Mapped[uuid.UUID] = mapped_column(
        UUID(), ForeignKey("user.tb_user.id_user", ondelete="SET NULL"), nullable=False
    )
