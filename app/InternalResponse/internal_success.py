from enum import Enum

from Enums.enums import LangEnum, ResponseCode
from fastapi import status as st
from InternalResponse.base_internal_response import BaseInternalResponses


class InternalSuccess(Enum):
    OK = st.HTTP_200_OK
    CREATED = st.HTTP_201_CREATED
    ACCEPTED = st.HTTP_202_ACCEPTED
    NO_CONTENT = st.HTTP_204_NO_CONTENT

    def __call__(self, language: LangEnum = LangEnum.EN_US) -> BaseInternalResponses:
        return BaseInternalResponses(rc=ResponseCode.OK, language=language, status_code=self.value)
