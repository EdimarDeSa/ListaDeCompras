import logging
from abc import ABC, abstractmethod

from sqlalchemy.orm import scoped_session, Session

from DataBase.connection_handler import create_session
from Repositories.user_repository import BaseRepository
from Validators.base_validator import BaseValidator


class BaseService(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass

    def create_db_session(self, write: bool = True) -> scoped_session[Session]:
        return create_session(write=write)

    @abstractmethod
    def _create_repository(self) -> type[BaseRepository]:
        pass

    @abstractmethod
    def _create_validator(self) -> type[BaseValidator]:
        pass

    @classmethod
    def create_logger(cls, name: str) -> logging.Logger:
        return logging.getLogger(name)
