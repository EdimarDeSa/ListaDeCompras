from logging import Logger, getLogger

from sqlalchemy.orm import scoped_session, Session

from app.DataBase.connection import DBConnectionHandler, get_db_url
from app.DataBase.models.dto_models import DefaultCategoryDTO
from app.Enums.enums import LangEnum
from app.Repositories.default_category_repository import DefaultCategoryRepository
from app.Services.base_service import BaseService
from app.Validators.base_validator import BaseValidator


class DefaultCategoryService(BaseService):
    def __init__(self) -> None:
        self._db_session = self._create_db_session()
        self._repository = self._create_repository()
        self._validator = self._create_validator()
        self._logger = self._create_logger()

    def read_all(self, language: LangEnum) -> list[DefaultCategoryDTO]:
        self._db_session = self._create_db_session()

        try:
            categories = self._repository.read_all(self._db_session, language)

            self._logger.debug(f"Categories found: {categories}")

            return categories

        except Exception as e:
            raise e

        finally:
            self._db_session.close()

    def _create_db_session(self) -> scoped_session[Session]:
        return DBConnectionHandler.create_session(db_url=get_db_url())

    def _create_repository(self) -> DefaultCategoryRepository:
        return DefaultCategoryRepository()

    def _create_validator(self) -> type[BaseValidator]:
        pass

    def _create_logger(self) -> Logger:
        return getLogger(__name__)
