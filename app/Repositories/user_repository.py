from uuid import UUID

from fastapi import status as st
from sqlalchemy.orm import Session, scoped_session

from app.Enums.base_internal_exception import BaseInternalException
from app.Enums.enums import LangEnum, ResponseCode
from app.Models.dto_models import UserDTO, NewUser, UpdateUserDTO
from app.Querys.user_querys import UserQuery
from app.Repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def read_all(self, db_session: scoped_session[Session], query_obj: UserQuery, language: LangEnum) -> list[UserDTO]:
        self.db_session = db_session
        try:

            query = query_obj.select_all_users()

            result = self.db_session.execute(query).all()

            if result is None:
                raise BaseInternalException(
                    rc=ResponseCode.USER_NOT_FOUND,
                    language=language,
                    status_code=st.HTTP_404_NOT_FOUND,
                )

            return [UserDTO.model_validate(row.User, from_attributes=True) for row in result]

        except Exception as e:
            raise e

    # noinspection PyTypeChecker
    def read_by_id(
        self, db_session: scoped_session[Session], query_obj: UserQuery, user_id: UUID, language: LangEnum
    ) -> UserDTO:
        self.db_session = db_session

        try:

            query = query_obj.select_user_by_id(user_id)

            result = self.db_session.execute(query).first()  # type: ignore

            if result is None:
                raise BaseInternalException(
                    rc=ResponseCode.USER_NOT_FOUND,
                    language=language,
                    status_code=st.HTTP_404_NOT_FOUND,
                )

            return UserDTO.model_validate(result[0])

        except Exception as e:
            raise e

    def create_user(self, db_session: scoped_session[Session], query_obj: UserQuery, new_user: NewUser) -> UserDTO:
        self.db_session = db_session

        try:

            query = query_obj.insert_user(**new_user.model_dump())

            self.db_session.execute(query)
            self.db_session.flush()

            return UserDTO.model_validate(new_user)

        except Exception as e:
            raise e

    def update_user(
        self, db_session: scoped_session[Session], query_obj: UserQuery, update_data: UpdateUserDTO
    ) -> UpdateUserDTO:
        self.db_session = db_session
        cleaned_data = self._clean_update_data(update_data)

        try:

            query = query_obj.select_user_by_id(update_data.id)

            result = self.db_session.execute(query).first()

            if result is None:
                raise BaseInternalException(
                    rc=ResponseCode.USER_NOT_FOUND,
                    language=update_data.language,
                    status_code=st.HTTP_404_NOT_FOUND,
                )

            query = query_obj.update_user_by_id(update_data.id, **cleaned_data)

            self.db_session.execute(query)
            self.db_session.flush()

            return UpdateUserDTO.model_validate(cleaned_data)

        except Exception as e:
            raise e

    @staticmethod
    def _clean_update_data(update_data: UpdateUserDTO) -> dict[str, UUID | str]:
        return {key: value for key, value in update_data.model_dump().items() if value is not None}
