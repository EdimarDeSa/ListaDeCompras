import logging
from abc import ABC, abstractmethod

from DataBase.querys import Query
from Enums.enums import ResponseCode, LangEnum


class BaseValidator(ABC):
    @classmethod
    def create_logger(cls, name: str) -> logging.Logger:
        return logging.getLogger(name)

    @classmethod
    def create_query(cls) -> Query:
        return Query()

    @abstractmethod
    def raise_error(self, error: ResponseCode, language: LangEnum) -> None:
        pass
