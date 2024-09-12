import uuid

from sqlalchemy import Select, Update, Insert, TextClause
from sqlalchemy import select, update, insert, text

from DataBase.models.defualt_product_models import DefaultProductDTO
from DataBase.schemas.default_category_schema import DefaultCategory
from DataBase.schemas.default_product_schema import DefaultProduct
from DataBase.schemas.unity_type_schema import UnityType
from DataBase.schemas.user_categories_schema import UserCategories
from DataBase.schemas.user_schema import TbUser


class Query:

    ### TEST ###
    @staticmethod
    def test_communication() -> TextClause[str]:
        return text("SELECT 1")

    ### USER TABLE ###
    def select_user_by_id(self, user_id: uuid.UUID) -> Select[TbUser]:
        return select(TbUser).where(TbUser.id == user_id)

    def select_user_by_email(self, email: str) -> Select[TbUser]:
        return select(TbUser).where(TbUser.email == email)

    def delete_user_by_id(self, user_id: uuid.UUID) -> Update[TbUser]:
        return update(TbUser).where(TbUser.id == user_id).values(is_active=False)

    def update_user_by_id(self, user_id: uuid.UUID, **kwargs: dict) -> Update[TbUser]:
        return update(TbUser).where(TbUser.id == user_id).values(**kwargs)

    def insert_user(self, **kwargs: dict) -> Insert[TbUser]:
        return insert(TbUser).values(**kwargs)

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
    def insert_user_categories(self, values: list[dict]) -> Insert[UserCategories]:
        return insert(UserCategories).values(values)

    def select_all_user_categories(self, user_id: uuid.UUID) -> Select[tuple[UserCategories]]:
        return select(UserCategories).where(UserCategories.user_id == user_id)
