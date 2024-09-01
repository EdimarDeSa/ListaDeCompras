from uuid import UUID

from sqlalchemy.orm import Session, scoped_session

from app.DataBase.models.dto_models import UserDTO, NewUser, UpdateUserDTO, UserLoginDTO
from app.Enums.enums import LangEnum, ResponseCode
from app.InternalResponse.internal_errors import InternalErrors
from app.Repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def read_all(self, db_session: scoped_session[Session], language: LangEnum) -> list[UserDTO]:
        self.db_session = db_session

        try:
            query = self.query.select_all_users()

            result = self.db_session.execute(query).all()

            if result is None:
                raise InternalErrors.NOT_FOUND_404(rc=ResponseCode.USER_NOT_FOUND, language=language)

            return [UserDTO.model_validate(row.User, from_attributes=True) for row in result]

        except Exception as e:
            self.return_db_error(e, language)

    # noinspection PyTypeChecker
    def read_by_id(self, db_session: scoped_session[Session], user_id: UUID, language: LangEnum) -> UserDTO:
        self.db_session = db_session

        try:
            query = self.query.select_user_by_id(user_id)

            result = self.db_session.execute(query).first()  # type: ignore

            if result is None:
                raise InternalErrors.NOT_FOUND_404(rc=ResponseCode.USER_NOT_FOUND, language=language)

            return UserDTO.model_validate(result.User)

        except Exception as e:
            self.return_db_error(e, language)

    def read_by_email(
        self,
        db_session: scoped_session[Session],
        user_email: str,
        to_login: bool = False,
        language: LangEnum = LangEnum.EN,
    ) -> UserDTO | UserLoginDTO:
        self.db_session = db_session

        try:
            query = self.query.select_user_by_email(user_email)

            result = self.db_session.execute(query).first()

            if result is None:
                raise InternalErrors.NOT_FOUND_404(rc=ResponseCode.USER_NOT_FOUND, language=language)

            if to_login:
                return UserLoginDTO.model_validate(result.User)
            return UserDTO.model_validate(result.User)

        except Exception as e:
            self.return_db_error(e, language)

    def create_user(self, db_session: scoped_session[Session], new_user: NewUser, language: LangEnum) -> UserDTO:
        self.db_session = db_session

        try:
            query = self.query.insert_user(**new_user.model_dump())

            self.db_session.execute(query)
            self.db_session.flush()

            return UserDTO.model_validate(new_user)

        except Exception as e:
            self.return_db_error(e, language)

    def update_user(
        self, db_session: scoped_session[Session], user_id: UUID, update_data: UpdateUserDTO, language: LangEnum
    ) -> UpdateUserDTO:
        self.db_session = db_session
        cleaned_data = self._clean_update_data(update_data)

        try:
            query = self.query.update_user_by_id(user_id, **cleaned_data)

            self.db_session.execute(query)
            self.db_session.flush()

            return UpdateUserDTO.model_validate(cleaned_data)

        except Exception as e:
            self.return_db_error(e, language)

    def delete_user_by_id(self, db_session: scoped_session[Session], user_id: UUID, language: LangEnum) -> None:
        self.db_session = db_session

        try:
            query = self.query.delete_user_by_id(user_id)

            self.db_session.execute(query)
            self.db_session.flush()

        except Exception as e:
            self.return_db_error(e, language)

    @staticmethod
    def _clean_update_data(update_data: UpdateUserDTO) -> dict[str, UUID | str]:
        return {key: value for key, value in update_data if value is not None}
