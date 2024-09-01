from enum import Enum

from fastapi import status as st

from app.Enums.enums import LangEnum, ResponseCode
from app.InternalResponse.base_internal_response import BaseInternalResponses


class InternalSuccess(Enum):
    OK = st.HTTP_200_OK
    CREATED = st.HTTP_201_CREATED
    ACCEPTED = st.HTTP_202_ACCEPTED
    NO_CONTENT = st.HTTP_204_NO_CONTENT

    def __call__(self, language: LangEnum = LangEnum.EN) -> BaseInternalResponses:
        return BaseInternalResponses(rc=ResponseCode.OK, language=language, status_code=self.value)
