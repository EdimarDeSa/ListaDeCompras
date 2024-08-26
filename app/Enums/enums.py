from enum import StrEnum, IntEnum


class LangEnum(StrEnum):
    PT_BR = "Pt_Br"
    EN = "En"


class ResponseCode(IntEnum):
    OK = 0

    EMAIL_EXISTS = -1
    EMAIL_INVALID = -2
    EMAIL_SAME = -3

    USER_NOT_FOUND = -4
    USER_ID_EXISTS = -5

    PASSWORD_NULL = -6
    PASSWORD_SAME = -7
    PASSWORD_LENGTH = -8
    PASSWORD_NEED_LOWER_CASE = -9
    PASSWORD_NEED_UPPER_CASE = -10
    PASSWORD_NEED_NUMBER = -11
    PASSWORD_NEED_SPECIAL_CHAR = -12

    NAME_LENGTH = -13
    NAME_NULL = -14

    UNKNOWN_ERROR = -999
