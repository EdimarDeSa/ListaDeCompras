import uuid

from sqlalchemy import select, insert, delete, update, Select, Delete, Update, Insert

from app.Models.models import User


class UserQuery:
    @staticmethod
    def select_all_users() -> Select[tuple[User]]:
        return select(User).order_by(User.name)

    @staticmethod
    def select_user_by_id(user_id: uuid.UUID) -> Select[User]:
        return select(User).where(User.id == user_id)

    @staticmethod
    def select_user_by_email(email: str) -> Select[User]:
        return select(User).where(User.email == email)

    @staticmethod
    def delete_user_by_id(user_id: uuid.UUID) -> Delete[User]:
        return delete(User).where(User.id == user_id)

    @staticmethod
    def update_user_by_id(user_id: uuid.UUID, **kwargs) -> Update[User]:
        return update(User).where(User.id == user_id).values(**kwargs)

    @staticmethod
    def insert_user(**kwargs) -> Insert[User]:
        return insert(User).values(**kwargs)
