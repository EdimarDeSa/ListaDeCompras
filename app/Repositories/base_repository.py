from abc import ABC
from typing import Optional

from sqlalchemy.orm import Session, scoped_session

from app.Enums.enums import ResponseCode
from app.InternalResponse.internal_errors import InternalErrors


class BaseRepository(ABC):
    __session: Optional[scoped_session[Session]] = None

    @property
    def db_session(self) -> Optional[scoped_session[Session]]:
        if self.__session is None:
            raise InternalErrors.INTERNAL_SERVER_ERROR_500(ResponseCode.DB_SESSION_NOT_SET)
        return self.__session

    @db_session.setter
    def db_session(self, session: scoped_session[Session]) -> None:
        if self.__session:
            raise InternalErrors.INTERNAL_SERVER_ERROR_500(ResponseCode.DB_SESSION_ALREADY_SET)
        self.__session = session
