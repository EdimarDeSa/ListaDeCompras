from abc import ABC

from fastapi import Response
from starlette.status import *

from app.Enums.enums import LangEnum, MessagesEnum, MsgLoader


class CustomHttpException(ABC, Response):
    def __init__(self, status_code: int, msg: MessagesEnum, lang: LangEnum) -> None:
        message = MsgLoader.get_message(msg, lang)
        super().__init__(status_code=status_code, content=message)


# TODO: Criar as mensagens deste response, adicionar o texto ao app.Enums.enums.MessagesEnum
class Ok(CustomHttpException):
    """:type: fastapi.Response(status_code: 200)"""

    def __init__(self, lang: LangEnum = LangEnum.PT_BR) -> None:
        super().__init__(status_code=HTTP_200_OK, msg="Ok", lang=lang)


# TODO: Criar as mensagens deste response, adicionar o texto ao app.Enums.enums.MessagesEnum
class Created(CustomHttpException):
    """:type: fastapi.Response(status_code: 201)"""

    def __init__(self, lang: LangEnum = LangEnum.PT_BR) -> None:
        super().__init__(status_code=HTTP_201_CREATED, msg="", lang=lang)


# TODO: Criar as mensagens deste response, adicionar o texto ao app.Enums.enums.MessagesEnum
class NoContent(CustomHttpException):
    """:type: fastapi.Response(status_code: 204)"""

    def __init__(self, lang: LangEnum = LangEnum.PT_BR) -> None:
        super().__init__(status_code=HTTP_204_NO_CONTENT, msg="", lang=lang)


class HttpResponses:
    Ok: type[Ok] = Ok
    NoContent: type[NoContent] = NoContent
    Created: type[Created] = Created
