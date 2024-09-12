from sqlalchemy import UniqueConstraint

from DataBase.schemas.base_schemas import BaseSchemaUserProperty


class Market(BaseSchemaUserProperty):
    __tablename__ = "market"

    __table_args__ = (UniqueConstraint("name", "user_id"),)
