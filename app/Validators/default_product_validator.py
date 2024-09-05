from logging import Logger, getLogger

from sqlalchemy.orm import scoped_session, Session

from app.DataBase.models.defualt_product_models import NewDefaultProduct
from app.Enums.enums import ResponseCode, LangEnum
from app.InternalResponse.internal_errors import InternalErrors
from app.Validators.base_validator import BaseValidator


class DefaultProductValidator(BaseValidator):
    def __init__(self):
        super(DefaultProductValidator, self).__init__()
        self._logger = self._create_logger()

    def validate_new_default_product(
        self, db_session: scoped_session[Session], new_product: NewDefaultProduct, language: LangEnum
    ):
        self.verify_if_name_does_not_exists(db_session, new_product.name, language)
        self.verify_if_default_unit_type_name_exists(db_session, new_product.unit_type_name, language)
        self.verify_if_default_category_name_exists(db_session, new_product.default_category_name, language)

    def _create_logger(self) -> Logger:
        return getLogger(__name__)

    def raise_error(self, error: ResponseCode, language: LangEnum) -> None:
        self._logger.exception(error)
        raise InternalErrors.BAD_REQUEST_400(error, language)

    def verify_if_name_does_not_exists(
        self, db_session: scoped_session[Session], name: str, language: LangEnum
    ) -> None:

        query = self.query.select_default_product_by_name(name)

        result = db_session.execute(query).first()

        if result is not None:
            self.raise_error(ResponseCode.PRODUCT_NAME_EXISTS, language)

    def verify_if_default_unit_type_name_exists(
        self, db_session: scoped_session[Session], unit_type_name: str, language: LangEnum
    ) -> None:
        self._logger.debug(f"Searching for {unit_type_name}")
        query = self.query.select_unity_type_by_name(unit_type_name)
        result = db_session.execute(query).first()
        self._logger.debug(f"Founded {result[0]}")

        if result is None:
            self.raise_error(ResponseCode.INVALID_UNIT_TYPE, language)

    def verify_if_default_category_name_exists(
        self, db_session: scoped_session[Session], category_name: str, language: LangEnum
    ) -> None:
        query = self.query.select_default_category_by_name(category_name)

        result = db_session.execute(query).first()

        if result is None:
            self.raise_error(ResponseCode.INVALID_CATEGORY, language)
