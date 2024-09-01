from logging import Logger

from sqlalchemy.orm import scoped_session, Session

from app.DataBase.connection import get_db_url, DBConnectionHandler
from app.DataBase.models.version_model import VersionModel
from app.Enums.enums import LangEnum
from app.InternalResponse.base_internal_response import BaseInternalResponses
from app.InternalResponse.internal_success import InternalSuccess
from app.Repositories.utils_repository import UtilsRepository
from app.Services.base_service import BaseService
from app.Validators.base_validator import BaseValidator


class UtilsService(BaseService):
    def __init__(self) -> None:
        self._repository = self._create_repository()
        self._logger = self._create_logger()

    def check_health(self, language: LangEnum) -> BaseInternalResponses:
        db_session = self._create_db_session()

        try:

            self._repository.check_health(db_session, language)

            return InternalSuccess.OK()

        except Exception as e:
            self._logger.exception(e)
            raise e

        finally:
            db_session.close()

    def get_version(self) -> VersionModel:
        version = "0.1.0"
        return VersionModel.from_string(version)

    def _create_repository(self) -> UtilsRepository:
        return UtilsRepository()

    def _create_validator(self) -> type[BaseValidator]:
        pass

    def _create_logger(self) -> Logger:
        return Logger(__name__)

    def _create_db_session(self) -> scoped_session[Session]:
        return DBConnectionHandler.create_session(db_url=get_db_url())
