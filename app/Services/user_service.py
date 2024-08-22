from logging import Logger
from uuid import UUID

from app.Enums.enums import LangEnum
from app.Models.dto_models import UserDTO
from app.Repositories.user_repository import UserRepository
from app.Services.base_service import BaseService
from app.Validators.user_validator import UserValidator


class UserService(BaseService):
    def __init__(self) -> None:
        self._repository = self.create_repository()
        self._validator = self.create_validator()
        self._logger = self.create_logger()
        pass

    def read_all(self, language: LangEnum) -> list[UserDTO]:
        try:
            users = self._repository.read_all(language)

            self._logger.debug(f"Users readed: {users}")
            return users
        except Exception as e:
            self._logger.exception(e)
            raise e

    def read_by_id(self, user_id: UUID, language: LangEnum) -> UserDTO:
        try:
            user = self._repository.read_by_id(user_id, language)

            self._logger.debug(f"Users readed: {user}")

            return user
        except Exception as e:
            self._logger.exception(e)
            raise e

    def create_repository(self) -> UserRepository:
        return UserRepository()

    def create_validator(self) -> UserValidator:
        return UserValidator()

    def create_logger(self) -> Logger:
        return Logger(__name__)
