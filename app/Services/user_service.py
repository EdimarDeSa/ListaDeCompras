from logging import Logger
from uuid import UUID

from sqlalchemy.orm import scoped_session, Session

from app.DataBase.connection import DBConnectionHandler, get_db_url
from app.DataBase.models.dto_models import UserDTO, NewUser, UpdateUserDTO
from app.Enums.enums import LangEnum
from app.Repositories.default_category_repository import DefaultCategoryRepository
from app.Repositories.user_repository import UserRepository
from app.Services.base_service import BaseService
from app.Validators.user_validator import UserValidator


class UserService(BaseService):
    def __init__(self) -> None:
        self._repository = self._create_repository()
        self._def_cat_repository = DefaultCategoryRepository()
        self._validator = self._create_validator()
        self._logger = self._create_logger()

    def read_all(self, language: LangEnum) -> list[UserDTO]:
        db_session = self._create_db_session()

        try:

            users = self._repository.read_all(db_session, language)

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
            self._logger.debug(f"Searching for user_id - {user_id}")
            user = self._repository.read_by_id(db_session, user_id, language)

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
            self._validator.validate_new_user(db_session, new_user, language)

            user = self._repository.create_user(db_session, new_user, language)

            self._logger.debug(f"User created: {user}")

            # self.active_user(db_session, user.id, language)

            db_session.commit()

            return user

        except Exception as e:
            db_session.rollback()
            self._logger.exception(e)

            raise e

        finally:
            db_session.close()

    def update_user(self, user_id: UUID, update_data: UpdateUserDTO, language: LangEnum) -> UpdateUserDTO:
        db_session = self._create_db_session()

        try:
            self._validator.validate_update_data(db_session, update_data, language)
            self._logger.debug(f"Updates validated")

            user = self._repository.update_user(db_session, user_id, update_data, language)
            self._logger.debug(f"User updated: {user_id}\nValues: {update_data.model_dump()}")

            db_session.commit()

            return user

        except Exception as e:
            db_session.rollback()
            self._logger.exception(e)

            raise e

        finally:
            db_session.close()

    def delete_user_by_id(self, user_id: UUID, language: LangEnum) -> None:
        db_session = self._create_db_session()

        try:

            self._repository.delete_user_by_id(db_session, user_id, language)

            db_session.commit()

        except Exception as e:
            db_session.rollback()
            self._logger.exception(e)

            raise e

        finally:
            db_session.close()

    def activate_user(self, db_session: scoped_session[Session], id_user: UUID, language: LangEnum) -> None:
        # Coleta as categorias padrões
        default_categories = self._def_cat_repository.read_all(db_session, language)

        # Registra as categorias para o usuário
        self._user_cat_repository.create_default_user_categories(db_session, id_user, default_categories, language)

        # Coleta todas as categorias do usuário
        user_categories = self._user_cat_repository.get_all_user_categories(db_session, id_user, language)

        # Coleta todos os produtos padrões
        default_products = self._def_prod_repository.get_all_default_products(db_session, language)

        # Registra produtos para o usuário
        self._user_prod_repository.create_default_user_products(
            db_session, id_user, default_products, user_categories, language
        )

    def _create_repository(self) -> UserRepository:
        return UserRepository()

    def _create_validator(self) -> UserValidator:
        return UserValidator()

    def _create_logger(self) -> Logger:
        return Logger(__name__)

    def _create_db_session(self) -> scoped_session[Session]:
        return DBConnectionHandler.create_session(db_url=get_db_url())

    def __call__(self, *args, **kwargs) -> None:
        self._logger.debug("Starting __call__")
        db_session = self._create_db_session()
        return self(db_session, *args, **kwargs)
