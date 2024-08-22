from abc import ABC, abstractmethod

from sqlalchemy.orm import Session


class BaseRepository(ABC):
    @abstractmethod
    def create_db_session(self) -> Session:
        pass
