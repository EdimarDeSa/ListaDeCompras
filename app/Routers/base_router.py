import logging
from abc import ABC, abstractmethod

from fastapi import APIRouter
from fastapi import status as st

from app.Enums.enums import ResponseCode
from app.InternalResponse.base_internal_response import BaseInternalResponses
from app.InternalResponse.internal_errors import InternalErrors
from app.Schemas.responses.base_response import BaseResponse, BaseContent
from app.Services.user_service import BaseService


class BaseRoutes(ABC):
    _router: APIRouter = None

    @abstractmethod
    def _create_service(self) -> type[BaseService]:
        pass

    @staticmethod
    def create_logger(name: str) -> logging.Logger:
        return logging.getLogger(name)

    @staticmethod
    def create_api_router(**kwargs) -> APIRouter:
        return APIRouter(**kwargs)

    @staticmethod
    def return_exception(e: Exception, **kwargs) -> BaseResponse:
        if isinstance(e, BaseInternalResponses):
            content = BaseContent(rc=e.rc, data=e.message)
            return BaseResponse(status_code=e.status_code, content=content, **kwargs)

        content = BaseContent(rc=ResponseCode.UNKNOWN_ERROR)
        return BaseResponse(status_code=st.HTTP_500_INTERNAL_SERVER_ERROR, content=content, **kwargs)

    @property
    def api_router(self):
        if self._router is None:
            raise InternalErrors.SERVICE_UNAVAILABLE_503(ResponseCode.ROUTER_NOT_DEFINED)
        return self._router

    @api_router.setter
    def api_router(self, value: APIRouter) -> None:
        if self._router is not None:
            raise InternalErrors.INTERNAL_SERVER_ERROR_500(ResponseCode.ROUTER_ALREADY_EXISTS)
        self._router = value
