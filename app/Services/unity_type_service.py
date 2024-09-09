import logging

from sqlalchemy.orm import scoped_session, Session

from app.DataBase.connection import DBConnectionHandler, get_db_url
from app.DataBase.models.dto_models import UnityTypeDTO
from app.Enums.enums import LangEnum
from app.Repositories.unity_type_repository import UnityTypeRepository
from app.Services.base_service import BaseService
from app.Validators.base_validator import BaseValidator


class UnityTypeService(BaseService):
    def __init__(self) -> None:
        self._repository = self._create_repository()
        self._validator = self._create_validator()
        self._logger = self._create_logger()

    def read_all(self, language: LangEnum) -> list[UnityTypeDTO]:
        db_session = self._create_db_session()
        self._logger.info("Starting read_all unity types")

        try:
            self._logger.debug("Trying to get all unity types")
            unity_types = self._repository.read_all(db_session, language)
            self._logger.info(f"Unity types found: {unity_types}")
            return unity_types

        except Exception as e:
            self._logger.exception(e)
            raise e

        finally:
            db_session.close()

    def read_by_name(self, unity_type_name: str, language: LangEnum) -> UnityTypeDTO:
        db_session = self._create_db_session()

        try:
            unity_type = self._repository.read_by_name(db_session, unity_type_name, language)
            return unity_type

        except Exception as e:
            self._logger.exception(e)
            raise e

        finally:
            db_session.close()

    def _create_db_session(self) -> scoped_session[Session]:
        return DBConnectionHandler.create_session(db_url=get_db_url())

    def _create_repository(self) -> UnityTypeRepository:
        return UnityTypeRepository()

    def _create_validator(self) -> type[BaseValidator]:
        pass

    def _create_logger(self) -> logging.Logger:
        return logging.getLogger(__name__)
