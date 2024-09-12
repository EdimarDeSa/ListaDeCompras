from typing import Any

from sqlalchemy import Sequence
from sqlalchemy.orm import scoped_session, Session

from DataBase.models.defualt_product_models import DefaultProductDTO, NewDefaultProduct
from DataBase.schemas.default_category_schema import DefaultCategory
from DataBase.schemas.default_product_schema import DefaultProduct
from DataBase.schemas.unity_type_schema import UnityType
from Enums.enums import LangEnum, ResponseCode
from InternalResponse.internal_errors import InternalErrors
from Repositories.base_repository import BaseRepository


class DefaultProductsRepository(BaseRepository):
    def __init__(self):
        self._query = self.create_query()
        self._logger = self.create_logger(__name__)

    def get_all_default_products(
        self, db_session: scoped_session[Session], language: LangEnum
    ) -> list[DefaultProductDTO]:
        self._logger.info("Starting get_all_default_products")

        try:
            self._logger.debug(f"Creating query to get all default products on table: {DefaultProduct.__tablename__}")
            query = self._query.select_all_default_products()

            self._logger.debug("Trying to get all default products")
            result: Sequence[list[DefaultProduct]] = db_session.execute(query).scalars().all()

            self._logger.debug(f"Default products found: {len(result)}")

            if result is None:
                self._logger.info("Default products not found")
                raise InternalErrors.NOT_FOUND_404(rc=ResponseCode.PRODUCT_NOT_FOUND, language=language)

            return [DefaultProductDTO.model_validate(product, from_attributes=True) for product in result]

        except Exception as e:
            self._logger.error(e)
            raise e

    def create_new_default_product(
        self, db_session: scoped_session[Session], new_product: NewDefaultProduct, language: LangEnum
    ):
        self._logger.info("Starting create_new_default_product")

        try:
            self._logger.debug("Preparing new default product to insert")
            cleaned_data = self._prepare_data_to_insert(db_session, new_product)
            self._logger.debug("Product prepared successfully")

            self._logger.debug(f"Creating query to get all default products on table: {DefaultProduct.__tablename__}")
            query = self._query.insert_default_product(**cleaned_data)

            db_session.execute(query)
            db_session.flush()

            self._logger.debug("Product inserted successfully")

            return DefaultProductDTO.model_validate(new_product)
        except Exception as e:
            self.return_db_error(e, language)

    def _prepare_data_to_insert(
        self, db_session: scoped_session[Session], new_product: NewDefaultProduct
    ) -> dict[str, Any]:
        cleaned_data: dict[str, Any] = new_product.model_dump(exclude_none=True)

        self._logger.debug(f"Searching for unity type where name = {new_product.unit_type_name}")
        query = self._query.select_unity_type_by_name(new_product.unit_type_name)
        unity_type_result: UnityType = db_session.execute(query).scalars().first()
        cleaned_data["unit_type_id"] = unity_type_result.id

        self._logger.debug(f"Searching for default category where name = {new_product.default_category_name}")
        query = self._query.select_default_category_by_name(new_product.default_category_name)
        default_category_result: DefaultCategory = db_session.execute(query).scalars().first()
        cleaned_data["default_category_id"] = default_category_result.id

        cleaned_data.pop("unit_type_name")
        cleaned_data.pop("default_category_name")

        return cleaned_data
