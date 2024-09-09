from enum import Enum

from fastapi import status as st

from app.Enums.enums import LangEnum, ResponseCode
from app.InternalResponse.base_internal_response import BaseInternalResponses


class InternalErrors(Enum):
    BAD_REQUEST_400 = st.HTTP_400_BAD_REQUEST
    UNAUTHORIZED_401 = st.HTTP_401_UNAUTHORIZED
    FORBIDDEN_403 = st.HTTP_403_FORBIDDEN
    NOT_FOUND_404 = st.HTTP_404_NOT_FOUND
    CONFLICT_409 = st.HTTP_409_CONFLICT
    INTERNAL_SERVER_ERROR_500 = st.HTTP_500_INTERNAL_SERVER_ERROR
    NOT_IMPLEMENTED_501 = st.HTTP_501_NOT_IMPLEMENTED
    BAD_GATEWAY_502 = st.HTTP_502_BAD_GATEWAY
    SERVICE_UNAVAILABLE_503 = st.HTTP_503_SERVICE_UNAVAILABLE
    GATEWAY_TIMEOUT_504 = st.HTTP_504_GATEWAY_TIMEOUT
    INVALID_MODEL_422 = st.HTTP_422_UNPROCESSABLE_ENTITY

    def __call__(self, rc: ResponseCode, language: LangEnum = LangEnum.EN_US) -> BaseInternalResponses:
        return BaseInternalResponses(rc=rc, language=language, status_code=self.value)
