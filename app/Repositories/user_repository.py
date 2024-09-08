from uuid import UUID

from sqlalchemy.orm import Session, scoped_session

from app.DataBase.models.dto_models import UserDTO, NewUser, UpdateUserDTO, UserLoginDTO
from app.DataBase.querys import Query
from app.DataBase.schemas.user_schema import User
from app.Enums.enums import LangEnum, ResponseCode
from app.InternalResponse.internal_errors import InternalErrors
from app.Repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self):
        self._query = Query()
        self._logger = self.create_logger(__name__)

    def read_all(self, db_session: scoped_session[Session], language: LangEnum) -> list[UserDTO]:
        try:
            self._logger.debug("Starting read_all")
            query = self._query.select_all_users()

            result = db_session.execute(query).all()

            if result is None:
                raise InternalErrors.NOT_FOUND_404(rc=ResponseCode.USER_NOT_FOUND, language=language)

            return [UserDTO.model_validate(row.User, from_attributes=True) for row in result]

        except Exception as e:
            self.return_db_error(e, language)

    # noinspection PyTypeChecker
    def read_by_id(self, db_session: scoped_session[Session], user_id: UUID, language: LangEnum) -> UserDTO:
        try:
            self._logger.debug(f"Searching user with id - '{user_id}' - in table - '{User.__tablename__}'")
            query = self._query.select_user_by_id(user_id)

            result = db_session.execute(query).first()  # type: ignore
            self._logger.debug(f"User found - {result.id}")

            if result is None:
                self._logger.debug("User not found")
                raise InternalErrors.NOT_FOUND_404(rc=ResponseCode.USER_NOT_FOUND, language=language)

            return UserDTO.model_validate(result.User)

        except Exception as e:
            self.return_db_error(e, language)

    def read_by_email(
        self,
        db_session: scoped_session[Session],
        user_email: str,
        to_login: bool = False,
        language: LangEnum = LangEnum.EN_US,
    ) -> UserDTO | UserLoginDTO:
        try:
            self._logger.debug(f"Searching user with email - '{user_email}' - in table - '{User.__tablename__}'")
            query = self._query.select_user_by_email(user_email)

            result: User = db_session.execute(query).scalars().first()
            self._logger.debug(f"User found - {result.id}")

            if result is None:
                self._logger.debug("User not found")
                raise InternalErrors.NOT_FOUND_404(rc=ResponseCode.USER_NOT_FOUND, language=language)

            if to_login:
                model = UserLoginDTO
            else:
                model = UserDTO
            self._logger.debug(f"Model selected: {model.__name__}")

            return model.model_validate(result)

        except Exception as e:
            self.return_db_error(e, language)

    def create_user(self, db_session: scoped_session[Session], new_user: NewUser, language: LangEnum) -> UserDTO:
        try:
            query = self._query.insert_user(**new_user.model_dump())

            db_session.execute(query)
            db_session.flush()

            return UserDTO.model_validate(new_user)

        except Exception as e:
            self.return_db_error(e, language)

    def update_user(
        self, db_session: scoped_session[Session], user_id: UUID, update_data: UpdateUserDTO, language: LangEnum
    ) -> UpdateUserDTO:
        try:
            cleaned_data = update_data.model_dump(exclude_none=True)
            query = self._query.update_user_by_id(user_id, **cleaned_data)

            db_session.execute(query)
            db_session.flush()

            return UpdateUserDTO.model_validate(cleaned_data)

        except Exception as e:
            self.return_db_error(e, language)

    def delete_user_by_id(self, db_session: scoped_session[Session], user_id: UUID, language: LangEnum) -> None:
        try:
            query = self._query.delete_user_by_id(user_id)

            db_session.execute(query)
            db_session.flush()

        except Exception as e:
            self.return_db_error(e, language)
