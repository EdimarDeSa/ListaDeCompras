from abc import ABC, abstractmethod
from logging import Logger

from app.Enums.enums import ResponseCode, LangEnum


class BaseValidator(ABC):
    @abstractmethod
    def _create_logger(self) -> Logger:
        pass

    @abstractmethod
    def raise_error(self, error: ResponseCode, language: LangEnum) -> None:
        pass
