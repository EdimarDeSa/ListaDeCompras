from typing import Protocol

MessageType = dict["LanguagesEnum", dict["ExceptionEnum", str]]


class BaseModelWithPassword(Protocol):
    password: str
