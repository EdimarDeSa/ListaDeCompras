import json
from enum import StrEnum
from pathlib import Path


class LangEnum(StrEnum):
    PT_BR = "Pt_Br"
    EN = "En"


class MessagesEnum(StrEnum):
    EMAIL_INVALID = "EmailInvalid"
    EMAIL_SAME = "EmailSame"
    PASSWORD_LENGHT = "PasswordLenght"
    PASSWORD_NEED_LOWER_CASE = "PasswordNeedLowerCase"
    PASSWORD_NEED_NUMBER = "PasswordNeedNumber"
    PASSWORD_NEED_SPECIAL = "PasswordNeedSpecial"
    PASSWORD_NEED_UPPER_CASE = "PasswordNeedUpperCase"
    PASSWORD_NULL = "PasswordNull"
    PASSWORD_SAME = "PasswordSame"
    USER_EMAIL_USED = "UserEmailUsed"
    USER_ID_EXISTS = "UserIdExists"
    USER_NOT_FOUND = "UserNotFound"


class MsgLoader:
    with open(Path(__file__).resolve().parent.parent.parent / "./messages.json", "r") as file:
        __messages = json.load(file)

    @classmethod
    def get_message(cls, error_code: MessagesEnum, language: LangEnum = LangEnum.PT_BR) -> str:
        return cls.__messages[language.value][error_code.value]


class HttpMethodsEnum(StrEnum):
    DELETE = "DELETE"
    GET = "GET"
    PATCH = "PATCH"
    POST = "POST"
    PUT = "PUT"
