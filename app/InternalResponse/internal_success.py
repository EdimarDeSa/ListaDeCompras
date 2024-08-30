from fastapi import status as st

from app.Enums.enums import LangEnum, ResponseCode
from app.InternalResponse.base_internal_response import BaseInternalResponses


class Ok(BaseInternalResponses):
    def __init__(self, language: LangEnum):
        super().__init__(rc=ResponseCode.OK, language=language, status_code=st.HTTP_200_OK)


class Created(BaseInternalResponses):
    def __init__(self, language: LangEnum):
        super().__init__(rc=ResponseCode.OK, language=language, status_code=st.HTTP_201_CREATED)


class Accepted(BaseInternalResponses):
    def __init__(self, language: LangEnum):
        super().__init__(rc=ResponseCode.OK, language=language, status_code=st.HTTP_202_ACCEPTED)


class NoContent(BaseInternalResponses):
    def __init__(self, language: LangEnum):
        super().__init__(rc=ResponseCode.OK, language=language, status_code=st.HTTP_204_NO_CONTENT)
