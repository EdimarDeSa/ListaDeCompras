from abc import ABC, abstractmethod

from fastapi import APIRouter
from fastapi import status as st

from app.Enums.base_internal_exception import BaseInternalException
from app.Enums.enums import ResponseCode
from app.Schemas.responses.base_response import BaseResponse, BaseContent
from app.Services.user_service import BaseService


class BaseRouter(ABC, APIRouter):
    @abstractmethod
    def create_service(self) -> type[BaseService]:
        pass

    @staticmethod
    def return_exception(e: Exception) -> BaseResponse:

        if isinstance(e, BaseInternalException):
            content = BaseContent(rc=e.rc, data=e.message)
            return BaseResponse(status_code=e.status_code, content=content)

        content = BaseContent(rc=ResponseCode.UNKNOWN_ERROR)
        return BaseResponse(status_code=st.HTTP_500_INTERNAL_SERVER_ERROR, content=content)
