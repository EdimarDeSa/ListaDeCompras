import logging
from typing import Any

from sqlalchemy.orm import scoped_session, Session

from app.DataBase.models.defualt_product_models import DefaultProductDTO, NewDefaultProduct
from app.Enums.enums import LangEnum, ResponseCode
from app.InternalResponse.internal_errors import InternalErrors
from app.Repositories.base_repository import BaseRepository


class DefaultProductsRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self._logger = logging.getLogger(__name__)

    def get_all_default_products(
        self, db_session: scoped_session[Session], language: LangEnum
    ) -> list[DefaultProductDTO]:
        self.db_session = db_session

        try:
            query = self._query.select_all_default_products()

            result = self.db_session.execute(query).all()

            if result is None:
                raise InternalErrors.NOT_FOUND_404(rc=ResponseCode.PRODUCT_NOT_FOUND, language=language)

            return [DefaultProductDTO.model_validate(p.DefaultProduct) for p in result]

        except Exception as e:
            raise e

    def create_new_default_product(
        self, db_session: scoped_session[Session], new_product: NewDefaultProduct, language: LangEnum
    ):
        self.db_session = db_session

        try:
            self._logger.debug("Preparing new default product to insert")
            cleaned_data = self._prepare_data_to_insert(new_product)
            self._logger.debug("Product prepared successfully")

            query = self._query.insert_default_product(**cleaned_data)

            self.db_session.execute(query)
            self.db_session.flush()

            return DefaultProductDTO.model_validate(new_product)
        except Exception as e:
            self.return_db_error(e, language)

    def _prepare_data_to_insert(self, new_product: NewDefaultProduct) -> dict[str, Any]:
        cleaned_data: dict[str, Any] = new_product.model_dump()

        self._logger.debug(f"Searching for unity type where name = {new_product.unit_type_name}")
        query = self._query.select_unity_type_by_name(new_product.unit_type_name)
        result = self.db_session.execute(query).first()
        cleaned_data["unit_type_id"] = result.UnityType.id

        self._logger.debug(f"Searching for default category where name = {new_product.default_category_name}")
        query = self._query.select_default_category_by_name(new_product.default_category_name)
        result = self.db_session.execute(query).first()
        cleaned_data["default_category_id"] = result.DefaultCategory.id

        cleaned_data.pop("unit_type_name")
        cleaned_data.pop("default_category_name")

        return cleaned_data
