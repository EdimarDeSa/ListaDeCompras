from abc import ABC, abstractmethod
from logging import Logger

from sqlalchemy.orm import scoped_session, Session

from app.Repositories.user_repository import BaseRepository
from app.Validators.base_validator import BaseValidator


class BaseService(ABC):
    @abstractmethod
    def _create_db_session(self) -> scoped_session[Session]:
        pass

    @abstractmethod
    def _create_repository(self) -> type[BaseRepository]:
        pass

    @abstractmethod
    def _create_validator(self) -> type[BaseValidator]:
        pass

    @abstractmethod
    def _create_logger(self) -> Logger:
        pass
