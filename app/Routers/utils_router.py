from fastapi import status as st

from app.Enums.enums import ResponseCode
from app.Enums.http_exceptions import InternalExceptions
from app.Models.version_model import VersionModel
from app.Routers.base_router import BaseRouter
from app.Schemas.responses.base_response import BaseResponse, BaseContent
from app.Services.utils_service import UtilsService


class UtilsRouter(BaseRouter):
    def __init__(self):
        super().__init__()
        self._service = self.create_service()

        self.register_routes()

    def register_routes(self):
        self.add_api_route("/utils/healthcheck", self.healthcheck, methods=["GET"])
        self.add_api_route("/utils/version", self.version, methods=["GET"])

    def healthcheck(self) -> BaseResponse:
        try:
            self._service.check_health()

        except InternalExceptions as e:
            content = BaseContent(rc=ResponseCode.OK, data=str(e))
            return BaseResponse(status_code=st.HTTP_500_INTERNAL_SERVER_ERROR, content=content)

        content = BaseContent(rc=ResponseCode.OK, data="OK")
        return BaseResponse(status_code=st.HTTP_200_OK, content=content)

    def version(self) -> BaseResponse:
        try:
            version: VersionModel = self._service.get_version()

        except InternalExceptions as e:
            content = BaseContent(rc=e.rc, data=str(e))
            return BaseResponse(status_code=st.HTTP_500_INTERNAL_SERVER_ERROR, content=content)

        content = BaseContent(rc=ResponseCode.OK, data=version)
        return BaseResponse(status_code=st.HTTP_200_OK, content=content)

    def create_service(self) -> UtilsService:
        return UtilsService()
