from sqlalchemy import UniqueConstraint

from app.DataBase.schemas.base_schema import BaseSchemaUserProperty


class UserCategories(BaseSchemaUserProperty):
    __tablename__ = "user_categories"

    __table_args__ = (UniqueConstraint("name", "user_id"),)
