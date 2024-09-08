import re

import email_validator
from passlib.context import CryptContext
from sqlalchemy.orm import scoped_session, Session

from app.DataBase.models.dto_models import NewUser, UpdateUserDTO
from app.DataBase.querys import Query
from app.Enums.enums import LangEnum, ResponseCode
from app.InternalResponse.internal_errors import InternalErrors
from app.Validators.base_validator import BaseValidator


class UserValidator(BaseValidator):
    def __init__(self):
        self._query = Query()
        self._logger = self._create_logger(__name__)
        self._pwd_context = CryptContext(schemes=["bcrypt"])

    def validate_new_user(self, db_session: scoped_session[Session], new_user: NewUser, language: LangEnum):
        self._validate_email(db_session, new_user.email, language)
        self._validate_password(new_user.password, language)
        self._validate_name(new_user.name, language)
        new_user.password = self._pwd_context.hash(new_user.password)

    def validate_update_data(
        self, db_session: scoped_session[Session], update_data: UpdateUserDTO, language: LangEnum
    ) -> None:
        if update_data.name is not None:
            self._validate_name(update_data.name, language)

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

    def _validate_email(self, db_session: scoped_session[Session], email: str, language: LangEnum) -> None:
        try:
            email_validator.validate_email(email, check_deliverability=False)

            query = self._query.select_user_by_email(email)

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

    def raise_error(self, error: ResponseCode, language: LangEnum) -> None:
        raise InternalErrors.BAD_REQUEST_400(error, language)

    def verify_password_hash(self, password: str, hashed_password: str, language: LangEnum) -> None:
        self._logger.debug("Verifying password hash")
        is_valid = self._pwd_context.verify(secret=password, hash=hashed_password)
        self._logger.debug(f"Password hash verified - <is_valid: {is_valid}>")

        if is_valid is False:
            self._logger.debug("Invalid password hash")
            raise InternalErrors.FORBIDDEN_403(ResponseCode.INVALID_CREDENTIALS, language)

    def hash_password(self, password: str) -> str:
        return self._pwd_context.hash(secret=password)

    def validate_user_active(self, is_active: bool, language: LangEnum) -> None:
        self._logger.debug(f"Validating if user is active - {is_active}")
        if is_active is False:
            self._logger.debug("User is not active")
            raise InternalErrors.FORBIDDEN_403(ResponseCode.USER_NOT_ACTIVE, language)
