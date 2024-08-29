import re
from logging import Logger

import email_validator
from fastapi import status as st
from passlib.context import CryptContext
from sqlalchemy.orm import scoped_session, Session

from app.Enums.base_internal_exception import BaseInternalException
from app.Enums.enums import LangEnum, ResponseCode
from app.Models.dto_models import NewUser, UpdateUserDTO
from app.Querys.user_querys import UserQuery
from app.Validators.base_validator import BaseValidator


class UserValidator(BaseValidator):
    def __init__(self):
        self._logger = self._create_logger()
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def validate_new_user(
        self, db_session: scoped_session[Session], query_obj: UserQuery, new_user: NewUser, language: LangEnum
    ):
        self._validate_email(db_session, query_obj, new_user.email, language)
        self._validate_password(new_user.password, language)
        self._validate_name(new_user.name, language)
        new_user.password = self._pwd_context.hash(new_user.password)

    def validate_update_data(
        self, db_session: scoped_session[Session], query_obj: UserQuery, update_data: UpdateUserDTO, language: LangEnum
    ) -> None:
        if update_data.name is not None:
            self._validate_name(update_data.name, language)

        if update_data.email is not None:
            self._validate_email(db_session, query_obj, update_data.email, language)

    def _validate_password(self, password: str, language: LangEnum) -> None:
        if not password:
            self.raise_error(ResponseCode.PASSWORD_NULL, language)

        if len(password) < 8:
            self.raise_error(ResponseCode.PASSWORD_LENGTH, language)

        if not re.search(r"\d", password):
            self.raise_error(ResponseCode.PASSWORD_NEED_NUMBER, language)

        if not re.search(r"[a-z]", password):
            self.raise_error(ResponseCode.PASSWORD_NEED_LOWER_CASE, language)

        if not re.search(r"[A-Z]", password):
            self.raise_error(ResponseCode.PASSWORD_NEED_UPPER_CASE, language)

        if not re.search(r"[\W_]", password):
            self.raise_error(ResponseCode.PASSWORD_NEED_SPECIAL_CHAR, language)

    def _validate_email(
        self, db_session: scoped_session[Session], query_obj: UserQuery, email: str, language: LangEnum
    ) -> None:
        try:
            email_validator.validate_email(email, check_deliverability=False)

            query = query_obj.select_user_by_email(email)

            result = db_session.execute(query).first()

            if result is not None:
                raise self.raise_error(ResponseCode.EMAIL_EXISTS, language)

        except Exception as e:
            self._logger.exception(e)
            self.raise_error(ResponseCode.EMAIL_INVALID, language)

    def _validate_name(self, name, language):
        if not name:
            self.raise_error(ResponseCode.NAME_LENGTH, language)

        if len(name) < 3:
            self.raise_error(ResponseCode.NAME_LENGTH, language)

        if len(name) > 100:
            self.raise_error(ResponseCode.NAME_LENGTH, language)

    def _create_logger(self) -> Logger:
        return Logger(__name__)

    def raise_error(self, error: ResponseCode, language: LangEnum) -> None:
        raise BaseInternalException(
            rc=error,
            language=language,
            status_code=st.HTTP_400_BAD_REQUEST,
        )

    def verify_password_hash(self, password: str, hashed_password: str, language: LangEnum) -> None:
        is_valid = self._pwd_context.verify(secret=password, hash=hashed_password)

        if is_valid is False:
            raise BaseInternalException(
                rc=ResponseCode.INVALID_CREDENTIALS,
                language=language,
                status_code=st.HTTP_400_BAD_REQUEST,
            )

    def hash_password(self, password: str) -> str:
        return self._pwd_context.hash(secret=password)
