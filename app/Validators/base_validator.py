import logging
from abc import ABC, abstractmethod

from app.Enums.enums import ResponseCode, LangEnum


class BaseValidator(ABC):
    @staticmethod
    def _create_logger(name: str) -> logging.Logger:
        return logging.getLogger(name)

    @abstractmethod
    def raise_error(self, error: ResponseCode, language: LangEnum) -> None:
        pass
