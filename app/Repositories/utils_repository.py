from sqlalchemy.orm import scoped_session, Session

from app.Enums.enums import ResponseCode, LangEnum
from app.InternalResponse.internal_errors import InternalErrors
from app.Repositories.base_repository import BaseRepository


class UtilsRepository(BaseRepository):
    def check_health(self, db_session: scoped_session[Session], language: LangEnum) -> None:
        self.db_session = db_session

        try:
            query = self._query.test_communication()

            result = self.db_session.execute(query).first()

            if result is None:
                raise InternalErrors.INTERNAL_SERVER_ERROR_500(ResponseCode.DB_ERROR, language)

        except Exception as e:
            raise e
