from app.Enums.enums import ResponseCode, LangEnum
from app.Utils.global_functions import MsgLoader


class BaseInternalResponses(Exception):
    def __init__(self, rc: ResponseCode, language: LangEnum, status_code: int = 500):
        self.rc = rc
        self.message = MsgLoader.get_message(rc, language)
        self.status_code = status_code
