from abc import ABC, abstractmethod
from logging import Logger

from app.DataBase.querys import Query
from app.Enums.enums import ResponseCode, LangEnum


class BaseValidator(ABC):
    def __init__(self):
        self.query = Query()

    @abstractmethod
    def _create_logger(self) -> Logger:
        pass

    @abstractmethod
    def raise_error(self, error: ResponseCode, language: LangEnum) -> None:
        pass
