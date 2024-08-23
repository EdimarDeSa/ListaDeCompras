from starlette.status import *

from app.Enums.base_http_response import BaseHttpResponse
from app.Enums.enums import LangEnum


class HttpResponses:
    Ok = Ok
    NoContent = NoContent
    Created = Created


# TODO: Criar as mensagens deste response, adicionar o texto ao app.Enums.enums.MessagesEnum
class Ok(BaseHttpResponse):
    """:type: fastapi.Response(status_code: 200)"""

    def __init__(self, lang: LangEnum = LangEnum.PT_BR) -> None:
        super().__init__(status_code=HTTP_200_OK, msg="Ok", lang=lang)


# TODO: Criar as mensagens deste response, adicionar o texto ao app.Enums.enums.MessagesEnum
class Created(BaseHttpResponse):
    """:type: fastapi.Response(status_code: 201)"""

    def __init__(self, lang: LangEnum = LangEnum.PT_BR) -> None:
        super().__init__(status_code=HTTP_201_CREATED, msg="", lang=lang)


# TODO: Criar as mensagens deste response, adicionar o texto ao app.Enums.enums.MessagesEnum
class NoContent(BaseHttpResponse):
    """:type: fastapi.Response(status_code: 204)"""

    def __init__(self, lang: LangEnum = LangEnum.PT_BR) -> None:
        super().__init__(status_code=HTTP_204_NO_CONTENT, msg="", lang=lang)
