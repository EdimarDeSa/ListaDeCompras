from enum import StrEnum, IntEnum


class LangEnum(StrEnum):
    PT_BR = "Pt_Br"
    EN = "En"


class ResponseCode(IntEnum):
    USER_EMAIL_EXISTS = -2
    USER_NOT_FOUND = -1
    OK = 0
    UNKNOWN_ERROR = -999


class MessagesEnum(StrEnum):
    EMAIL_INVALID = "EmailInvalid"
    EMAIL_SAME = "EmailSame"
    PASSWORD_LENGTH = "PasswordLenght"
    PASSWORD_NEED_LOWER_CASE = "PasswordNeedLowerCase"
    PASSWORD_NEED_NUMBER = "PasswordNeedNumber"
    PASSWORD_NEED_SPECIAL = "PasswordNeedSpecial"
    PASSWORD_NEED_UPPER_CASE = "PasswordNeedUpperCase"
    PASSWORD_NULL = "PasswordNull"
    PASSWORD_SAME = "PasswordSame"
    USER_EMAIL_USED = "UserEmailUsed"
    USER_ID_EXISTS = "UserIdExists"
    USER_NOT_FOUND = "UserNotFound"


class HttpMethodsEnum(StrEnum):
    DELETE = "DELETE"
    GET = "GET"
    PATCH = "PATCH"
    POST = "POST"
    PUT = "PUT"
