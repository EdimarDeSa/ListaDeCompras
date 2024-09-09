import os
from datetime import timedelta
from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import scoped_session, Session

from app.DataBase.connection import DBConnectionHandler, get_db_url
from app.DataBase.models.dto_models import UserLoginDTO
from app.DataBase.models.token_model import Token, TokenData
from app.Enums.enums import ResponseCode, LangEnum
from app.InternalResponse.base_internal_response import BaseInternalResponses
from app.InternalResponse.internal_errors import InternalErrors
from app.Repositories.user_repository import UserRepository
from app.Services.base_service import BaseService
from app.Utils.global_functions import datetime_now_utc
from app.Validators.user_validator import UserValidator

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthService(BaseService):
    def __init__(self) -> None:
        self._repository = self._create_repository()
        self._validator = self._create_validator()
        self._logger = self.create_logger(__name__)

    def authenticate_user(self, user_email: str, password: str, language: LangEnum) -> Token:
        db_session = self._create_db_session()
        self._logger.debug("Starting authenticate_user")

        try:
            self._logger.debug(f"Searching user - {user_email}")
            user: UserLoginDTO = self._repository.read_by_email(db_session, user_email, True, language)
            self._logger.debug(f"User found - <result: {user}>")

            self._logger.debug(f"Validating user - {user.id}")
            self._validator.validate_user_active(user.is_active, language)

            self._logger.debug(f"Password verification - {user.id}")
            self._validator.verify_password_hash(password, user.password, language)

            self._logger.debug(f"Authentication success for user - {user.id}")
            token = self.create_access_token(user)

            return token

        except Exception as e:
            if isinstance(e, BaseInternalResponses):
                self._logger.exception(f"Matching response code - {e.rc}")
                if e.rc == ResponseCode.USER_NOT_FOUND:
                    e.rc = ResponseCode.INVALID_CREDENTIALS
            raise e

        finally:
            db_session.close()

    def create_access_token(self, user: UserLoginDTO) -> Token:
        self._logger.debug("Starting create_access_token")

        self._logger.debug("Creating token expire time")
        expire: int = self.__get_expire_time()
        self._logger.debug(f"Token expire time created - {expire}")

        self._logger.debug("Creating token data")
        token_data: TokenData = TokenData(exp=expire, **user.model_dump())
        self._logger.debug(f"Token data created for user - {token_data.id}")

        self._logger.debug("Encoding token data")
        to_encode: dict = token_data.model_dump(mode="json", by_alias=True)

        encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
        self._logger.debug(f"Token data dict - {encoded_jwt}")

        token = Token(access_token=encoded_jwt, token_type="bearer")
        self._logger.info(f"Token created - {token}")

        return token

    def refresh_jwt_token(self, refresh_token: str, language: LangEnum) -> Token:
        """
        Atualiza o token JWT se o token de atualização fornecido for válido.
        """
        try:
            self._logger.info(f"Starting refresh token: {refresh_token}")
            decoded_data: dict = jwt.decode(
                jwt=refresh_token,
                key=os.getenv("SECRET_KEY"),
                algorithms=[os.getenv("ALGORITHM")],
            )
            self._logger.debug("Token data decoded")

            self._logger.debug("Turning token data into UserLoginDTO")
            user_login = UserLoginDTO(**decoded_data)
            new_token = self.create_access_token(user_login)
            self._logger.debug(f"Success refresh token - created token")
            return new_token

        except jwt.ExpiredSignatureError:
            self._logger.exception("Token expired")
            raise InternalErrors.UNAUTHORIZED_401(ResponseCode.TOKEN_EXPIRED, language)
        except jwt.InvalidTokenError:
            self._logger.exception("Invalid token")
            raise InternalErrors.UNAUTHORIZED_401(ResponseCode.INVALID_TOKEN, language)

    def _create_db_session(self) -> scoped_session[Session]:
        return DBConnectionHandler.create_session(db_url=get_db_url())

    def _create_repository(self) -> UserRepository:
        return UserRepository()

    def _create_validator(self) -> UserValidator:
        return UserValidator()

    def __get_expire_time(self) -> int:
        expires_delta = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15)))
        expires_time = datetime_now_utc() + expires_delta
        return int(expires_time.timestamp())


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
