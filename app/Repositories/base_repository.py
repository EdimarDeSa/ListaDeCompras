import logging
from abc import ABC

from sqlalchemy.exc import SQLAlchemyError

from app.Enums.enums import ResponseCode, LangEnum
from app.InternalResponse.internal_errors import InternalErrors


class BaseRepository(ABC):
    @staticmethod
    def return_db_error(error: Exception, language: LangEnum) -> None:
        if isinstance(error, SQLAlchemyError):
            raise InternalErrors.INTERNAL_SERVER_ERROR_500(rc=ResponseCode.DB_ERROR, language=language)
        raise error

    @staticmethod
    def create_logger(name: str) -> logging.Logger:
        return logging.getLogger(name)
