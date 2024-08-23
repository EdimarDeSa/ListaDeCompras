from abc import ABC

from starlette.status import *

from app.Enums.enums import LangEnum, MessagesEnum, ResponseCode
from app.Utils.global_functions import MsgLoader


class BaseInternalException(ABC, Exception):
    def __init__(self, status_code: int, error_message: MessagesEnum, lang: LangEnum, rc: ResponseCode) -> None:
        super().__init__()
        self.message: str = MsgLoader.get_message(error_message, lang)
        self.status_code: int = status_code
        self.rc: ResponseCode = rc


class UserNotFound(BaseInternalException):
    def __init__(self, lang: LangEnum = LangEnum.PT_BR) -> None:
        super().__init__(
            status_code=HTTP_404_NOT_FOUND,
            error_message=MessagesEnum.USER_NOT_FOUND,
            lang=lang,
            rc=ResponseCode.USER_NOT_FOUND,
        )


class UserEmailUsed(BaseInternalException):
    def __init__(self, lang: LangEnum = LangEnum.PT_BR) -> None:
        super().__init__(
            status_code=HTTP_400_BAD_REQUEST,
            error_message=MessagesEnum.USER_EMAIL_USED,
            lang=lang,
            rc=ResponseCode.USER_EMAIL_EXISTS,
        )


class InternalExceptions:
    UserNotFound = UserNotFound
    UserEmailUsed = UserEmailUsed
