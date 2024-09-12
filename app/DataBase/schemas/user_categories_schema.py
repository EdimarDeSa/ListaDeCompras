from sqlalchemy import UniqueConstraint

from DataBase.schemas.base_schemas import BaseSchemaUserProperty


class UserCategories(BaseSchemaUserProperty):
    __tablename__ = "user_category"
    __table_args__ = (UniqueConstraint("name", "user_id"),)
