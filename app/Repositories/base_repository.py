from abc import ABC
from typing import Optional

from sqlalchemy.orm import Session, scoped_session


class BaseRepository(ABC):
    __session: Optional[scoped_session[Session]] = None

    @property
    def db_session(self) -> Optional[scoped_session[Session]]:
        if self.__session is None:
            raise Exception("Session not set")
        return self.__session

    @db_session.setter
    def db_session(self, session: scoped_session[Session]) -> None:
        self.__session = session
