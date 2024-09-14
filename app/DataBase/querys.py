import uuid

from sqlalchemy import Select, Update, Insert, TextClause, Delete, delete
from sqlalchemy import select, update, insert, text

from DataBase.models.defualt_product_models import DefaultProductDTO
from DataBase.schemas.default_category_schema import DefaultCategory
from DataBase.schemas.default_product_schema import DefaultProduct
from DataBase.schemas.unity_type_schema import UnityType
from DataBase.schemas.user_categories_schema import UserCategory
from DataBase.schemas.user_products_schema import UserProduct
from DataBase.schemas.user_schema import User


class Query:

    ### TEST ###
    @staticmethod
    def test_communication() -> TextClause[str]:
        return text("SELECT 1")

    ### USER TABLE ###
    def select_user_by_id(self, user_id: uuid.UUID) -> Select[User]:
        return select(User).where(User.id == user_id)

    def select_user_by_email(self, email: str) -> Select[User]:
        return select(User).where(User.email == email)

    def delete_user_by_id(self, user_id: uuid.UUID) -> Delete[User]:
        return delete(User).where(User.id == user_id)

    def update_user_by_id(self, user_id: uuid.UUID, **kwargs: dict) -> Update[User]:
        return update(User).where(User.id == user_id).values(**kwargs)

    def insert_user(self, user_data: dict) -> Insert[User]:
        return insert(User).values(user_data)

    ### UNITY TYPE TABLE ###
    def select_all_unity_types(self) -> Select[tuple[UnityType]]:
        return select(UnityType).order_by(UnityType.name)

    def select_unity_type_by_name(self, unity_type_name: str) -> Select[UnityType]:
        return select(UnityType).where(UnityType.name == unity_type_name)

    ### DEFAULT CATEGORY TABLE ###
    def select_all_default_categories(self) -> Select[tuple[DefaultCategory]]:
        return select(DefaultCategory).order_by(DefaultCategory.name)

    def select_default_category_by_name(self, default_category_name: str) -> Select[DefaultCategory]:
        return select(DefaultCategory).where(DefaultCategory.name == default_category_name)

    ### DEFAULT PRODUCT TABLE ###
    def select_all_default_products(self) -> Select[tuple[DefaultProduct]]:
        return select(DefaultProduct).order_by(DefaultProduct.name)

    def select_default_product_by_name(self, default_product_name: str) -> Select[DefaultProduct]:
        return select(DefaultProduct).where(DefaultProduct.name == default_product_name)

    def insert_default_product(self, **kwargs: dict) -> Insert[DefaultProductDTO]:
        return insert(DefaultProduct).values(**kwargs)

    ### USER CATEGORIES TABLE ###
    def select_all_user_categories(self, user_id: uuid.UUID) -> Select[tuple[UserCategory]]:
        return select(UserCategory).where(UserCategory.user_id == user_id)

    def select_user_categories_by_ids(self, inserted_ids: list[uuid.UUID]) -> Select[tuple[UserCategory]]:
        return select(UserCategory).where(UserCategory.id.in_(inserted_ids))

    def insert_user_product(self, user_products_data: dict) -> Insert[UserProduct]:
        return insert(UserProduct).values(user_products_data)

    def select_all_default_categories_names(self) -> Select[tuple[DefaultCategory.name]]:
        return select(DefaultCategory.name).order_by(DefaultCategory.name)

    def insert_user_category(self, user_cat_data: dict) -> Insert[UserCategory]:
        return insert(UserCategory).values(user_cat_data)

    def select_user_category_id_by_name(self, user_id: uuid.UUID, name: str) -> Select[UserCategory.id]:
        return select(UserCategory.id).where(UserCategory.user_id == user_id and UserCategory.name == name)
