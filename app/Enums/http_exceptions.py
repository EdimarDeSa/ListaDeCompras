from abc import ABC

from fastapi import HTTPException
from starlette.status import *

from app.Enums.enums import LangEnum, MsgLoader, MessagesEnum


class CustomHttpException(ABC, HTTPException):
    def __init__(self, status_code: int, error_code: MessagesEnum, lang: LangEnum) -> None:
        message = MsgLoader.get_message(error_code, lang)
        super().__init__(status_code=status_code, detail=message)


class UserNotFound(CustomHttpException):
    def __init__(self, lang: LangEnum = LangEnum.PT_BR) -> None:
        super().__init__(status_code=HTTP_404_NOT_FOUND, error_code=MessagesEnum.USER_NOT_FOUND, lang=lang)


class UserEmailUsed(CustomHttpException):
    def __init__(self, lang: LangEnum = LangEnum.PT_BR) -> None:
        super().__init__(status_code=HTTP_400_BAD_REQUEST, error_code=MessagesEnum.USER_EMAIL_USED, lang=lang)


class HttpExceptions:
    UserNotFound: type[UserNotFound] = UserNotFound
    UserEmailUsed: type[UserEmailUsed] = UserEmailUsed
