from abc import ABC, abstractmethod
from logging import Logger

from app.Repositories.user_repository import BaseRepository
from app.Validators.base_validator import BaseValidator


class BaseService(ABC):
    @abstractmethod
    def create_repository(self) -> type[BaseRepository]:
        pass

    @abstractmethod
    def create_validator(self) -> type[BaseValidator]:
        pass

    @abstractmethod
    def create_logger(self) -> Logger:
        pass
