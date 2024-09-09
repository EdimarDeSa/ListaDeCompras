from typing import Protocol


MessageType = dict["LanguagesEnum", dict["ExceptionEnum", str]]


METHODS = ["get", "post", "put", "delete"]


class BaseModelWithPassword(Protocol):
    password: str
