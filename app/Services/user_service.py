from logging import Logger
from uuid import UUID

from sqlalchemy.orm import scoped_session, Session

from app.DbConnection.connection import DBConnectionHandler, get_db_url
from app.Enums.enums import LangEnum
from app.Models.dto_models import UserDTO, NewUser, UpdateUserDTO
from app.Querys.user_querys import UserQuery
from app.Repositories.user_repository import UserRepository
from app.Services.base_service import BaseService
from app.Validators.user_validator import UserValidator


class UserService(BaseService):
    def __init__(self) -> None:
        self._repository = self._create_repository()
        self._validator = self._create_validator()
        self._query = self._create_query()
        self._logger = self._create_logger()

    def read_all(self, language: LangEnum) -> list[UserDTO]:
        db_session = self._create_db_session()

        try:

            users = self._repository.read_all(db_session, self._query, language)

            self._logger.debug(f"Users found: {users}")

            db_session.commit()

            return users

        except Exception as e:
            self._logger.exception(e)
            raise e

        finally:
            db_session.close()

    def read_by_id(self, user_id: UUID, language: LangEnum) -> UserDTO:
        db_session = self._create_db_session()

        try:
            user = self._repository.read_by_id(db_session, self._query, user_id, language)

            self._logger.debug(f"User found: {user}")

            return user

        except Exception as e:
            self._logger.exception(e)
            raise e

        finally:
            db_session.close()

    def create_user(self, new_user: NewUser, language: LangEnum) -> UserDTO:
        db_session = self._create_db_session()

        try:
            self._validator.validate_new_user(db_session, self._query, new_user, language)

            user = self._repository.create_user(db_session, self._query, new_user)

            self._logger.debug(f"User created: {user}")

            db_session.commit()

            return user

        except Exception as e:
            db_session.rollback()

            self._logger.exception(e)

            raise e

        finally:
            db_session.close()

    def update_user(self, update_data: UpdateUserDTO, language: LangEnum) -> UpdateUserDTO:
        db_session = self._create_db_session()

        try:
            self._validator.validate_update_data(db_session, self._query, update_data, language)

            user = self._repository.update_user(db_session, self._query, update_data)

            self._logger.debug(f"User updates: {update_data.model_dump()}")

            db_session.commit()

            return user

        except Exception as e:
            db_session.rollback()

            self._logger.exception(e)

            raise e

        finally:
            db_session.close()

    def delete_user_by_email(self, user_email: str) -> None:
        db_session = self._create_db_session()

        try:

            self._repository.delete_user_by_email(db_session, self._query, user_email)

            db_session.commit()

        except Exception as e:
            db_session.rollback()

            self._logger.exception(e)

            raise e

        finally:
            db_session.close()

    def _create_repository(self) -> UserRepository:
        return UserRepository()

    def _create_validator(self) -> UserValidator:
        return UserValidator()

    def _create_logger(self) -> Logger:
        return Logger(__name__)

    def _create_query(self) -> UserQuery:
        return UserQuery()

    def _create_db_session(self) -> scoped_session[Session]:
        return DBConnectionHandler.create_session(db_url=get_db_url())
