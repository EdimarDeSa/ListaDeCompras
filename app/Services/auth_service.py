import os
from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from DataBase.models.dto_models import UserLoginDTO
from DataBase.models.token_model import Token, TokenData
from Enums.enums import ResponseCode, LangEnum
from InternalResponse.base_internal_response import BaseInternalResponses
from InternalResponse.internal_errors import InternalErrors
from Repositories.user_repository import UserRepository
from Services.base_service import BaseService
from Validators.user_validator import UserValidator

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthService(BaseService):
    def __init__(self) -> None:
        self._repository = self._create_repository()
        self._validator = self._create_validator()
        self._logger = self.create_logger(__name__)

    def authenticate_user(self, user_email: str, password: str, language: LangEnum) -> Token:
        self._logger.debug("Starting authenticate_user")

        self._logger.debug("Creating db session")
        db_session = self.create_db_session()

        try:

            self._logger.debug(f"Searching user by <Email: {user_email}>")
            user: UserLoginDTO = self._repository.read_by_email(db_session, user_email, True, language)
            self._logger.debug(f"User found - <result: {user}>")

            self._logger.debug(f"Check if user is active")
            self._validator.check_if_user_is_active(user, language)
            self._logger.debug(f"User is active")

            self._logger.debug(f"Check if password is valid")
            self._validator.check_password_hash(password, user.password, language)
            self._logger.debug(f"Password is valid")

            self._logger.debug(f"Creating token")
            token = self.create_access_token(user)
            self._logger.debug(f"Authentication success for user - {user.id}")

            return token

        except Exception as e:
            self._logger.info(f"Checking if error is instance of {BaseInternalResponses.__name__}")
            if isinstance(e, BaseInternalResponses):
                self._logger.info(f"Checking if response code is {ResponseCode.USER_NOT_FOUND.name}")
                if e.rc == ResponseCode.USER_NOT_FOUND:
                    self._logger.info(
                        f"Change error to:"
                        f" {InternalErrors.FORBIDDEN_403.name} with {ResponseCode.INVALID_CREDENTIALS.name}"
                    )
                    raise InternalErrors.FORBIDDEN_403(ResponseCode.INVALID_CREDENTIALS, language)
            raise e

        finally:
            db_session.close()

    def create_access_token(self, user_data: [UserLoginDTO | TokenData]) -> Token:
        self._logger.info("Starting create_access_token")

        self._logger.debug("Creating token data")
        token_data = TokenData.model_validate(user_data, from_attributes=True)
        self._logger.debug(f"Token data created for user - {token_data.id}")
        self._logger.debug(f"Token expires in {token_data.expire_date()}")

        self._logger.debug("Encoding token data")
        to_encode: dict = token_data.model_dump(mode="json", by_alias=True)

        encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
        self._logger.debug(f"Token encoded")

        token = Token(access_token=encoded_jwt, token_type="bearer")
        self._logger.debug(f"Token created - {token}")

        return token

    def refresh_jwt_token(self, current_token: str, language: LangEnum) -> Token:
        """
        Update the JWT token if the provided token is valid.
        """
        self._logger.info(f"Starting refresh_jwt_token")

        try:
            decoded_data: dict = jwt.decode(
                jwt=current_token,
                key=os.getenv("SECRET_KEY"),
                algorithms=[os.getenv("ALGORITHM")],
            )
            self._logger.debug("Token data decoded")

            self._logger.debug("Validate model UserLoginDTO")
            token_data = TokenData.model_validate(decoded_data)

            self._logger.debug("Generating new token")
            new_token: Token = self.create_access_token(token_data)
            self._logger.debug(f"Success refresh token - created token")
            return new_token

        except jwt.ExpiredSignatureError:
            self._logger.exception("Token expired")
            raise InternalErrors.UNAUTHORIZED_401(ResponseCode.TOKEN_EXPIRED, language)
        except jwt.InvalidTokenError:
            self._logger.exception("Invalid token")
            raise InternalErrors.UNAUTHORIZED_401(ResponseCode.INVALID_TOKEN, language)

    def _create_repository(self) -> UserRepository:
        return UserRepository()

    def _create_validator(self) -> UserValidator:
        return UserValidator()


def decode_token(token: Annotated[Token, Depends(oauth2_scheme)]) -> TokenData:
    try:
        payload: dict = jwt.decode(
            jwt=token,
            key=os.getenv("SECRET_KEY"),
            algorithms=[os.getenv("ALGORITHM")],
        )

        current_user = TokenData.model_validate(payload)

        if current_user.is_active is False:
            raise InternalErrors.UNAUTHORIZED_401(ResponseCode.INVALID_CREDENTIALS, LangEnum.EN_US)

        return current_user
    except Exception as e:
        raise e
