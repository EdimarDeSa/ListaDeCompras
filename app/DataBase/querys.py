import uuid

from sqlalchemy import Select, Update, Insert, TextClause
from sqlalchemy import select, update, insert, text

from app.DataBase.models.defualt_product_models import DefaultProductDTO
from app.DataBase.schemas.default_category_schema import DefaultCategory
from app.DataBase.schemas.default_product_schema import DefaultProduct
from app.DataBase.schemas.unity_type_schema import UnityType
from app.DataBase.schemas.user_schema import User


class Query:

    ### TEST ###
    @staticmethod
    def test_communication() -> TextClause[str]:
        return text("SELECT 1")

    ### USER TABLE ###
    @staticmethod
    def select_user_by_id(user_id: uuid.UUID) -> Select[User]:
        return select(User).where(User.id == user_id)

    @staticmethod
    def select_user_by_email(email: str) -> Select[User]:
        return select(User).where(User.email == email)

    @staticmethod
    def delete_user_by_id(user_id: uuid.UUID) -> Update[User]:
        return update(User).where(User.id == user_id).values(is_active=False)

    @staticmethod
    def update_user_by_id(user_id: uuid.UUID, **kwargs) -> Update[User]:
        return update(User).where(User.id == user_id).values(**kwargs)

    @staticmethod
    def insert_user(**kwargs) -> Insert[User]:
        return insert(User).values(**kwargs)

    ### UNITY TYPE TABLE ###
    @staticmethod
    def select_all_unity_types() -> Select[tuple[UnityType]]:
        return select(UnityType).order_by(UnityType.name)

    @staticmethod
    def select_unity_type_by_name(unity_type_name: str) -> Select[UnityType]:
        return select(UnityType).where(UnityType.name == unity_type_name)

    ### DEFAULT CATEGORY TABLE ###
    @staticmethod
    def select_all_default_categories() -> Select[tuple[DefaultCategory]]:
        return select(DefaultCategory).order_by(DefaultCategory.name)

    @staticmethod
    def select_default_category_by_name(default_category_name: str) -> Select[DefaultCategory]:
        return select(DefaultCategory).where(DefaultCategory.name == default_category_name)

    ### DEFAULT PRODUCT TABLE ###
    @staticmethod
    def select_all_default_products() -> Select[tuple[DefaultProduct]]:
        return select(DefaultProduct).order_by(DefaultProduct.name)

    @staticmethod
    def select_default_product_by_name(default_product_name: str) -> Select[DefaultProduct]:
        return select(DefaultProduct).where(DefaultProduct.name == default_product_name)

    @staticmethod
    def insert_default_product(**kwargs) -> Insert[DefaultProductDTO]:
        return insert(DefaultProduct).values(**kwargs)
