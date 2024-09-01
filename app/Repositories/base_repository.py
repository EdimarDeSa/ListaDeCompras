from abc import ABC
from typing import Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, scoped_session

from app.DataBase.querys import Query
from app.Enums.enums import ResponseCode, LangEnum
from app.InternalResponse.internal_errors import InternalErrors


class BaseRepository(ABC):
    __session: Optional[scoped_session[Session]] = None

    def __init__(self):
        self.query = Query()

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

    def return_db_error(self, error: Exception, language: LangEnum) -> None:
        if isinstance(error, SQLAlchemyError):
            raise InternalErrors.INTERNAL_SERVER_ERROR_500(rc=ResponseCode.DB_ERROR, language=language)
        raise error
