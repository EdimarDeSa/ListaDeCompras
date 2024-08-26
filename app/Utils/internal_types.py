from app.Enums.enums import LangEnum
from app.Utils.global_functions import MsgLoader


# class ErrorsDict(dict):
#     def __init__(self):
#         super().__init__()
#
#     def insert(self, err: MessagesEnum, lang: LangEnum) -> None:
#         self[err] = MsgLoader.get_message(err, lang)


MessageType = dict["LanguagesEnum", dict["ExceptionEnum", str]]
