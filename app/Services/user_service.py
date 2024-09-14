from uuid import UUID

from sqlalchemy.orm import scoped_session, Session

from DataBase.models.dto_models import (
    UserDTO,
    NewUser,
    UpdateUserDTO,
    UpdateUserEmailDTO,
    UpdateUserPasswordDTO,
)
from Enums.enums import LangEnum
from Repositories.default_category_repository import DefaultCategoryRepository
from Repositories.default_products_repository import DefaultProductsRepository
from Repositories.user_categories_repository import UserCategoriesRepository
from Repositories.user_products_repository import UserProductsRepository
from Repositories.user_repository import UserRepository
from Services.base_service import BaseService
from Validators.user_validator import UserValidator


class UserService(BaseService):
    def __init__(self):
        self._repository = self._create_repository()
        self._def_cat_repository = DefaultCategoryRepository()
        self._user_cat_repository = UserCategoriesRepository()
        self._user_prod_repository = UserProductsRepository()
        self._def_prod_repository = DefaultProductsRepository()
        self._validator = self._create_validator()
        self._logger = self.create_logger(__name__)

    def read_by_id(self, user_id: UUID, language: LangEnum) -> UserDTO:
        db_session = self.create_db_session()

        try:
            self._logger.debug(f"Searching for user_id - {user_id}")
            user = self._repository.read_by_id(db_session, user_id, language)
            self._logger.debug(f"User found: {user}")

            return user

        except Exception as e:
            raise e

        finally:
            db_session.close()

    def create_user(self, new_user: NewUser, language: LangEnum) -> UserDTO:
        self._logger.info(f"Starting create_user")

        db_session = self.create_db_session()

        try:
            self._logger.debug(f"Validating new user data")
            self._validator.validate_new_user(db_session, new_user, language)

            self._logger.debug(f"Saving new user: {new_user.email}")
            user: UserDTO = self._repository.create_user(db_session, new_user, language)

            self._logger.debug(f"User created: {user}")

            self._logger.debug(f"Activating user: {user.id}")
            self.activate_user(db_session, user.id, language)
            self._logger.debug(f"User activated: {user.id}")

            db_session.commit()

            return user

        except Exception as e:
            db_session.rollback()
            raise e

        finally:
            db_session.close()

    def update_user(self, user_id: UUID, update_data: UpdateUserDTO, language: LangEnum) -> UpdateUserDTO:
        db_session = self.create_db_session()

        try:
            self._logger.debug(f"Validating updates")
            self._validator.validate_update_data(update_data, language)
            self._logger.debug(f"Updates validated")

            user = self._repository.update_user(db_session, user_id, update_data, language)
            self._logger.debug(f"User updated: {user_id}\nValues: {update_data.model_dump()}")

            db_session.commit()

            return user

        except Exception as e:
            db_session.rollback()
            raise e

        finally:
            db_session.close()

    def update_user_email(self, user_id: UUID, new_email: UpdateUserEmailDTO, language: LangEnum) -> None:
        db_session = self.create_db_session()

        try:
            self._logger.debug(f"Validating updates")
            self._validator.validate_email(db_session, new_email.email, language)
            self._logger.debug(f"Updates validated")

            self._repository.update_user(db_session, user_id, new_email, language)
            self._logger.debug(f"User updated: {user_id} - new email: {new_email}")

            db_session.commit()
            self._logger.info(f"User updated: {user_id} - new email: {new_email}")

        except Exception as e:
            db_session.rollback()
            raise e

        finally:
            db_session.close()

    def update_user_password(self, user_id: UUID, new_password: UpdateUserPasswordDTO, language: LangEnum) -> None:
        db_session = self.create_db_session()

        try:
            self._logger.debug(f"Validating updates")
            self._validator.validate_password(new_password, language)
            self._logger.debug(f"Updates validated")

            self._repository.update_user(db_session, user_id, new_password, language)

            db_session.commit()
            self._logger.info(f"User updated: {user_id}")

        except Exception as e:
            db_session.rollback()
            raise e

        finally:
            db_session.close()

    def delete_user_by_id(self, user_id: UUID, language: LangEnum) -> None:
        self._logger.info(f"Starting delete_user_by_id")
        db_session = self.create_db_session()

        try:
            self._logger.debug(f"Deleting user: {user_id}")
            self._repository.delete_user_by_id(db_session, user_id, language)

            self._logger.info(f"User deleted: {user_id}")

            db_session.commit()

        except Exception as e:
            db_session.rollback()
            raise e

        finally:
            db_session.close()

    def activate_user(self, db_session: scoped_session[Session], user_id: UUID, language: LangEnum) -> None:
        self._logger.info(f"Activating user: {user_id}")

        self._logger.debug("Creating user categories")
        self._user_cat_repository.create_default_user_categories(db_session, user_id, language)

        self._logger.debug("Creating user products")
        self._user_prod_repository.create_default_user_products(db_session, user_id, language)
        self._logger.debug("User products created")

        self._logger.info(f"User activated: {user_id}")

    def _create_repository(self) -> UserRepository:
        return UserRepository()

    def _create_validator(self) -> UserValidator:
        return UserValidator()
