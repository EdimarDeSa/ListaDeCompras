import os
from datetime import timedelta
from logging import Logger
from typing import Annotated

import jwt
from app.ResponseCode.base_internal_exception import BaseInternalResponses
from fastapi import Depends
from fastapi import status as st
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import scoped_session, Session

from app.DbConnection.connection import DBConnectionHandler, get_db_url
from app.Enums.enums import ResponseCode, LangEnum
from app.Models.dto_models import UserLoginDTO
from app.Models.token_model import Token, TokenData
from app.Querys.user_querys import UserQuery
from app.Repositories.user_repository import UserRepository
from app.Services.base_service import BaseService
from app.Utils.global_functions import datetime_now_utc
from app.Validators.user_validator import UserValidator

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthService(BaseService):

    def __init__(self) -> None:
        self._db_session = self._create_db_session()
        self._repository = self._create_repository()
        self._validator = self._create_validator()
        self._logger = self._create_logger()
        self._query = self._create_query()

    def authenticate_user(self, user_email: str, password: str, language: LangEnum) -> Token:
        self._logger.info("Starting authenticate_user")

        try:
            user: UserLoginDTO = self._repository.read_by_email(
                db_session=self._db_session,
                query_obj=self._query,
                user_email=user_email,
                to_login=True,
                language=language,
            )

            self._validator.verify_password_hash(password=password, hashed_password=user.password, language=language)

            token = self.create_access_token(user=user)
            return token

        except Exception as e:
            self._logger.exception(e)
            if isinstance(e, BaseInternalResponses):
                if e.rc == ResponseCode.USER_NOT_FOUND:
                    e.rc = ResponseCode.INVALID_CREDENTIALS
            raise e

        finally:
            self._db_session.close()

    def create_access_token(self, user: UserLoginDTO) -> Token:
        expire: int = self.__get_expire_time()

        token_data: TokenData = TokenData(exp=expire, **user.model_dump())

        to_encode: dict = token_data.model_dump(mode="json", by_alias=True)

        encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))

        token = Token(access_token=encoded_jwt, token_type="bearer")
        self._logger.info(token)
        return token

    @staticmethod
    def decode_token(token: Annotated[Token, Depends(oauth2_scheme)]) -> TokenData:
        try:
            payload: dict = jwt.decode(
                jwt=token,
                key=os.getenv("SECRET_KEY"),
                algorithms=[os.getenv("ALGORITHM")],
            )

            current_user = TokenData.model_validate(payload)

            if current_user.is_active is False:
                raise BaseInternalResponses(
                    rc=ResponseCode.INVALID_CREDENTIALS,
                    language=LangEnum.EN,
                    status_code=st.HTTP_400_BAD_REQUEST,
                )

            return current_user
        except Exception as e:
            raise e

    def _create_db_session(self) -> scoped_session[Session]:
        return DBConnectionHandler.create_session(db_url=get_db_url())

    def _create_repository(self) -> UserRepository:
        return UserRepository()

    def _create_validator(self) -> UserValidator:
        return UserValidator()

    def _create_logger(self) -> Logger:
        return Logger(__name__)

    def _create_query(self) -> UserQuery:
        return UserQuery()

    def __get_expire_time(self) -> int:
        expires_delta = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15)))
        expires_time = datetime_now_utc() + expires_delta
        return int(expires_time.timestamp())


decode_token = AuthService.decode_token
