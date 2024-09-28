from DataBase.models.defualt_product_models import NewDefaultProduct
from DataBase.schemas.default_category_schema import DefaultCategory
from DataBase.schemas.default_product_schema import DefaultProduct
from DataBase.schemas.unity_type_schema import UnityType
from Enums.enums import LangEnum, ResponseCode
from InternalResponse.internal_errors import InternalErrors
from sqlalchemy.orm import Session, scoped_session
from Validators.base_validator import BaseValidator


class DefaultProductValidator(BaseValidator):
    def __init__(self):
        self._logger = self.create_logger(__name__)
        self._query = self.create_query()

    def validate_new_default_product(
        self, db_session: scoped_session[Session], new_product: NewDefaultProduct, language: LangEnum
    ):
        self._logger.info("Starting validate_new_default_product")

        self.verify_if_name_does_not_exists(db_session, new_product.name, language)
        self.verify_if_default_unit_type_name_exists(db_session, new_product.unit_type_name, language)
        self.verify_if_default_category_name_exists(db_session, new_product.default_category_name, language)

        self._logger.info("Product validated")

    def raise_error(self, error: ResponseCode, language: LangEnum) -> None:
        self._logger.exception(error)
        raise InternalErrors.BAD_REQUEST_400(error, language)

    def verify_if_name_does_not_exists(
        self, db_session: scoped_session[Session], name: str, language: LangEnum
    ) -> None:
        self._logger.info("Verifying if name exists")
        query = self._query.select_default_product_by_name(name)

        self._logger.debug(f"Searching for {name}")
        result: DefaultProduct = db_session.execute(query).scalars().first()
        self._logger.info(f"Founded {result}")

        if result is not None:
            self.raise_error(ResponseCode.PRODUCT_NAME_EXISTS, language)

    def verify_if_default_unit_type_name_exists(
        self, db_session: scoped_session[Session], unit_type_name: str, language: LangEnum
    ) -> None:
        self._logger.info(f"Verifying if {unit_type_name} exists")
        query = self._query.select_unity_type_by_name(unit_type_name)

        self._logger.debug(f"Searching for {unit_type_name}")
        result: UnityType = db_session.execute(query).scalars().first()
        self._logger.info(f"Founded {result}")

        if result is None:
            self.raise_error(ResponseCode.INVALID_UNIT_TYPE, language)

    def verify_if_default_category_name_exists(
        self, db_session: scoped_session[Session], category_name: str, language: LangEnum
    ) -> None:
        self._logger.info(f"Verifying if {category_name} exists")
        query = self._query.select_default_category_by_name(category_name)

        self._logger.debug(f"Searching for {category_name}")
        result: DefaultCategory = db_session.execute(query).scalars().first()
        self._logger.info(f"Founded {result}")

        if result is None:
            self.raise_error(ResponseCode.INVALID_CATEGORY, language)
