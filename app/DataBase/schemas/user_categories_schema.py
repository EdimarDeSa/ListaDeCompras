from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, relationship

from DataBase.schemas.base_schemas import BaseSchemaUserProperty


class UserCategory(BaseSchemaUserProperty):
    __tablename__ = "user_category"
    __table_args__ = (UniqueConstraint("name", "user_id"),)

    user: Mapped[list["User"]] = relationship(
        "User",
        viewonly=True,
        back_populates="categories",
    )
