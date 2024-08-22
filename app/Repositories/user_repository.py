from sqlite3 import Row
from uuid import UUID

from sqlalchemy import select, Sequence
from sqlalchemy.orm import Session

from app.DbConnection.connection import get_db_url, DBConnectionHandler
from app.Enums.enums import LangEnum
from app.Enums.http_exceptions import InternalExceptions
from app.Models.dto_models import UserDTO
from app.Models.models import User
from app.Repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def read_all(self, language: LangEnum) -> list[UserDTO]:
        session = None

        try:
            session = self.create_db_session()
            query = select(User).order_by(User.name)

            result: Sequence[Row] = session.execute(query).all()

            if result is None:
                raise InternalExceptions.UserNotFound(language)

            return [UserDTO.model_validate(row[0], from_attributes=True) for row in result]
        except Exception as e:
            raise e
        finally:
            try:
                session.close()
            except Exception as e:
                raise e

    def read_by_id(self, user_id: UUID, language: LangEnum) -> UserDTO:
        session = None

        try:
            session = self.create_db_session()
            query = select(User).where(User.id == user_id)

            result: Row = session.execute(query).first()

            if result is None:
                raise InternalExceptions.UserNotFound(language)

            return UserDTO.model_validate(result[0])
        except Exception as e:
            raise e
        finally:
            try:
                session.close()
            except Exception as e:
                raise e

    def create_db_session(self) -> Session:
        return DBConnectionHandler.create_session(db_url=get_db_url())
