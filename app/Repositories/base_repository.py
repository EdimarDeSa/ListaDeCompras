from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy.orm import Session, scoped_session


class BaseRepository(ABC):
    __session: Optional[scoped_session[Session]] = None

    @property
    def session(self) -> Optional[scoped_session[Session]]:
        if self.__session is None:
            raise Exception("Session not set")
        return self.__session

    @session.setter
    def session(self, session: scoped_session[Session]) -> None:
        self.__session = session

    @abstractmethod
    def create_db_session(self) -> scoped_session[Session]:
        pass
