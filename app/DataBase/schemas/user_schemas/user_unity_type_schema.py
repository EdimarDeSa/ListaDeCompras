import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base_schema import BaseSchemaUserItem


class UserUnitTypeSchema(BaseSchemaUserItem):
    __tablename__ = "tb_user_unit_type"
    __table_args__ = (
        {"schema": "user"},
        UniqueConstraint("name", "cd_user", name="unique_unit_type_name_per_user"),
        UniqueConstraint("abbreviation", "cd_user", name="unique_unit_type_abbreviation_per_user"),
    )

    id_user_unit_type: Mapped[uuid.UUID] = mapped_column(uuid.UUID(), primary_key=True, default_factory=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(length=50), nullable=False, unique=True)
    abbreviation: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)
    base_calc: Mapped[int] = mapped_column(Integer(), nullable=False, default=1)
    last_update: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    creation: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))

    # default_products: Mapped[list["DefaultProduct"]] = relationship("DefaultProduct", back_populates="unity_type")
