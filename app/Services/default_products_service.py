from DataBase.connection_handler import DBConnectionHandler, get_db_url
from DataBase.models.defualt_product_models import DefaultProductDTO, NewDefaultProduct
from Enums.enums import LangEnum
from Repositories.default_products_repository import DefaultProductsRepository
from Services.base_service import BaseService
from sqlalchemy.orm import Session, scoped_session
from Validators.default_product_validator import DefaultProductValidator


class DefaultProductsService(BaseService):
    def __init__(self) -> None:
        self._repository = self._create_repository()
        self._validator = self._create_validator()
        self._logger = self.create_logger(__name__)

    def get_all_default_products(self, language: LangEnum) -> list[DefaultProductDTO]:
        db_session = self._create_db_session()

        self._logger.info("Starting get_all_default_products")

        try:
            self._logger.debug("Trying to get all default products")
            products: list[DefaultProductDTO] = self._repository.get_all_default_products(db_session, language)

            self._logger.debug(f"Default products found: {len(products)}")

            return products
        except Exception as e:
            raise e

        finally:
            db_session.close()

    def create_new_default_product(self, new_product: NewDefaultProduct, language: LangEnum) -> DefaultProductDTO:
        db_session = self._create_db_session()

        try:
            self._logger.debug("Validating new default product")
            self._validator.validate_new_default_product(db_session, new_product, language)
            self._logger.debug("Product validated")

            product = self._repository.create_new_default_product(db_session, new_product, language)
            self._logger.debug(f"Default product created: {product}")

            db_session.commit()

            return product

        except Exception as e:
            self._logger.error(f"An error occurred while retrieving default products: {e}")
            db_session.rollback()
            raise e

        finally:
            db_session.close()

    def _create_db_session(self) -> scoped_session[Session]:
        return DBConnectionHandler.create_session(db_url=get_db_url())

    def _create_repository(self) -> DefaultProductsRepository:
        return DefaultProductsRepository()

    def _create_validator(self) -> DefaultProductValidator:
        return DefaultProductValidator()
