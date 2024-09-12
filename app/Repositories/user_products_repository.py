from uuid import UUID

from sqlalchemy.orm import Session, scoped_session

from DataBase.models.defualt_product_models import DefaultProductDTO
from DataBase.models.dto_models import UserCategoryDTO
from Enums.enums import LangEnum
from Repositories.base_repository import BaseRepository


class UserProductsRepository(BaseRepository):
    def __init__(self):
        self._query = self.create_query()
        self._logger = self.create_logger(__name__)

    def create_default_user_products(
        self,
        db_session: scoped_session[Session],
        user_id: UUID,
        default_products: list[DefaultProductDTO],
        user_categories: list[UserCategoryDTO],
        language: LangEnum,
    ) -> None:
        def iterate_user_unity_types(name: str) -> UUID:
            pass

        self._logger.info("Starting create_default_user_products")

        # try:
        #     self._logger.debug("Creating user products data")
        #     new_products = [
        #         NewUserProduct(
        #             user_id=user_id,
        #             name=prod.name,
        #             image_url=prod.image_url,
        #             unity_types_id=,
        #             price_unity_types_id=prod.unit_type_name,
        #             category_id=,
        #         )
        #          for prod in default_products
        #     ]
        pass
