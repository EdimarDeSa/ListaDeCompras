from abc import ABC

from fastapi import Response

from app.Enums.enums import LangEnum, MessagesEnum, ResponseCode
from app.Utils.global_functions import MsgLoader


class BaseHttpResponse(ABC, Response):
    def __init__(self, status_code: int, msg: MessagesEnum, lang: LangEnum, rc: ResponseCode) -> None:
        super().__init__()
        self.message: str = MsgLoader.get_message(msg, lang)
        self.status_code: int = status_code
        self.rc: ResponseCode = rc
