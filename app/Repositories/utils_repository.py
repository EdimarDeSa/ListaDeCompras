from sqlalchemy.orm import scoped_session, Session

from app.Enums.enums import ResponseCode, LangEnum
from app.InternalResponse.internal_errors import InternalErrors
from app.Repositories.base_repository import BaseRepository


class UtilsRepository(BaseRepository):
    def __init__(self):
        self._query = self.create_query()
        self._logger = self.create_logger(__name__)

    def check_health(self, db_session: scoped_session[Session], language: LangEnum) -> None:

        try:

            query = self._query.test_communication()

            result = db_session.execute(query).scalars().first()
            self._logger.info(f"Health check result: {result}")

            if result is None:
                self._logger.error("Health check failed!")
                raise InternalErrors.INTERNAL_SERVER_ERROR_500(ResponseCode.DB_ERROR, language)

        except Exception as e:
            raise e
