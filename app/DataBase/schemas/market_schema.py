from sqlalchemy import UniqueConstraint

from app.DataBase.schemas.base_schema import BaseSchemaUserProperty


class Market(BaseSchemaUserProperty):
    __tablename__ = "market"

    __table_args__ = (UniqueConstraint("name", "user_id"),)
