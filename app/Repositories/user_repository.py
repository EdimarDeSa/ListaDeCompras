from sqlite3 import Row
from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, scoped_session

from app.DbConnection.connection import get_db_url, DBConnectionHandler
from app.Enums.enums import LangEnum
from app.Enums.http_exceptions import InternalExceptions
from app.Models.dto_models import UserDTO
from app.Models.models import User
from app.Repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):

    def read_all(self, language: LangEnum) -> list[UserDTO]:

        try:

            self.session = self.create_db_session()

            query = select(User).order_by(User.name)

            result = self.session.execute(query).all()

            if result is None:
                raise InternalExceptions.UserNotFound(language)

            return [UserDTO.model_validate(row[0], from_attributes=True) for row in result]

        except Exception as e:
            raise e

        finally:

            try:
                self.session.close()

            except Exception as e:
                raise e

    # noinspection PyTypeChecker
    def read_by_id(self, user_id: UUID, language: LangEnum) -> UserDTO:
        session: scoped_session[Session | Any]

        try:

            self.session = self.create_db_session()

            query = select(User).where(User.id == user_id)

            result: Row = self.session.execute(query).first()  # type: ignore

            if result is None:
                raise InternalExceptions.UserNotFound(language)

            return UserDTO.model_validate(result[0])

        except Exception as e:
            raise e

        finally:

            try:
                self.session.close()

            except Exception as e:
                raise e

    def create_db_session(self) -> scoped_session[Session]:
        return DBConnectionHandler.create_session(db_url=get_db_url())
