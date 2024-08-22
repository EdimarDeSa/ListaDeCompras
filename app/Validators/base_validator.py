from abc import ABC, abstractmethod
from logging import Logger


class BaseValidator(ABC):
    @abstractmethod
    def create_logger(self) -> Logger:
        pass
