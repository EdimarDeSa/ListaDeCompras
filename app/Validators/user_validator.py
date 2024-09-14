import re

import email_validator
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import scoped_session, Session

from DataBase.models.dto_models import NewUser, UpdateUserDTO, UserLoginDTO
from DataBase.schemas.user_schema import User
from Enums.enums import LangEnum, ResponseCode
from InternalResponse.internal_errors import InternalErrors
from Utils.internal_types import BaseModelWithPassword
from Validators.base_validator import BaseValidator


class UserValidator(BaseValidator):
    def __init__(self):
        self._logger = self.create_logger(__name__)
        self._query = self.create_query()
        self._pwd_context = CryptContext(schemes=["bcrypt"])

    def validate_new_user(self, db_session: scoped_session[Session], new_user: NewUser, language: LangEnum):
        self._logger.info("Starting validate_new_user")

        self.validate_email(db_session, new_user.email, language)
        self.validate_password(new_user, language)
        self._validate_name(new_user.name, language)

        self._logger.info("New user is validated")

    def validate_update_data(self, update_data: UpdateUserDTO, language: LangEnum) -> None:
        if update_data.name is not None:
            self._logger.debug("Validating name")
            self._validate_name(update_data.name, language)

    def validate_password(self, model_with_password: BaseModelWithPassword, language: LangEnum) -> None:
        if not isinstance(model_with_password, BaseModel):
            raise InternalErrors.INVALID_MODEL_422(ResponseCode.INVALID_MODEL, language)

        password = model_with_password.password
        self._logger.info("Validating password")

        self._logger.debug("Checking if password is not null")
        if not password:
            self.raise_error(ResponseCode.PASSWORD_NULL, language)

        self._logger.debug("Checking if password length is greater than 8")
        if len(password) < 8:
            self.raise_error(ResponseCode.PASSWORD_LENGTH, language)

        self._logger.debug("Checking if password has number")
        if not re.search(r"\d", password):
            self.raise_error(ResponseCode.PASSWORD_NEED_NUMBER, language)

        self._logger.debug("Checking if password has special character")
        if not re.search(r"[a-z]", password):
            self.raise_error(ResponseCode.PASSWORD_NEED_LOWER_CASE, language)

        self._logger.debug("Checking if password has uppercase character")
        if not re.search(r"[A-Z]", password):
            self.raise_error(ResponseCode.PASSWORD_NEED_UPPER_CASE, language)

        self._logger.debug("Checking if password has special character")
        if not re.search(r"[\W_]", password):
            self.raise_error(ResponseCode.PASSWORD_NEED_SPECIAL_CHAR, language)

        self._logger.info("Password is valid")

        self._logger.debug("Hashing password")
        model_with_password.password = self._pwd_context.hash(password)

    def validate_email(self, db_session: scoped_session[Session], email: str, language: LangEnum) -> None:
        self._logger.info("Starting validate_email")

        try:
            self._logger.debug("Check if email is valid and deliverable")
            email_validator.validate_email(email, check_deliverability=True)
            self._logger.debug("Email is valid and deliverable")

            query = self._query.select_user_by_email(email)

            self._logger.debug(f"Checking if email - '{email}' - exists in table - '{User.__tablename__}'")
            result: User = db_session.execute(query).scalar()
            self._logger.debug(f"User found - <user: {result}>")

            if result is not None:
                self._logger.info("Email already exists")
                self.raise_error(ResponseCode.EMAIL_EXISTS, language)

            self._logger.info("Email is valid")

        except Exception as e:
            if isinstance(e, email_validator.EmailNotValidError):
                self._logger.debug("Email is not valid")
                self.raise_error(ResponseCode.EMAIL_INVALID, language)
            raise e

    def _validate_name(self, name, language):
        self._logger.info("Validating name")

        self._logger.debug("Checking if name is not null")
        if not name:
            self.raise_error(ResponseCode.NAME_LENGTH, language)

        self._logger.debug("Checking if name length is greater than 3")
        if len(name) < 3:
            self.raise_error(ResponseCode.NAME_LENGTH, language)

        self._logger.debug("Checking if name length is less than 100")
        if len(name) > 100:
            self.raise_error(ResponseCode.NAME_LENGTH, language)

        self._logger.info("Name is valid")

    def raise_error(self, error: ResponseCode, language: LangEnum) -> None:
        raise InternalErrors.BAD_REQUEST_400(error, language)

    def check_password_hash(self, password: str, hashed_password: str, language: LangEnum) -> None:
        self._logger.debug("Verifying password hash...")
        is_valid = self._pwd_context.verify(secret=password, hash=hashed_password)
        self._logger.debug(f"Password hash verified - <is_valid: {is_valid}>")

        if is_valid is False:
            self._logger.warning("Invalid password")
            raise InternalErrors.FORBIDDEN_403(ResponseCode.INVALID_CREDENTIALS, language)

    def hash_password(self, password: str) -> str:
        return self._pwd_context.hash(secret=password)

    def check_if_user_is_active(self, user: UserLoginDTO, language: LangEnum) -> None:
        self._logger.debug(f"Validating if user is active - {user.is_active}")
        if user.is_active is False:
            self._logger.warning(f"User {user.id} is not active")
            raise InternalErrors.FORBIDDEN_403(ResponseCode.USER_NOT_ACTIVE, language)
