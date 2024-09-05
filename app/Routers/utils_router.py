from fastapi import status as st, Request
from starlette.responses import RedirectResponse

from app.DataBase.models.version_model import VersionModel
from app.Enums.enums import ResponseCode, LangEnum
from app.Routers.base_router import BaseRoutes
from app.Schemas.responses.base_response import BaseResponse, BaseContent
from app.Services.utils_service import UtilsService


class UtilsRoutes(BaseRoutes):
    def __init__(self):
        self.api_router = self.create_api_router(tags=["Utils"])
        self._service = self._create_service()

        self.register_routes()

    def register_routes(self):
        self._router.add_api_route("/health", self.health, methods=["GET"])
        self._router.add_api_route("/version", self.version, methods=["GET"])
        self._router.add_api_route("/", self.home, methods=["GET"])

    def health(self, request: Request) -> BaseResponse:
        try:
            result = self._service.check_health(LangEnum.EN_US)

            content = BaseContent(rc=0, data=result.message)
            return BaseResponse(status_code=200, content=content)

        except Exception as e:
            self.return_exception(e)

    def version(self, request: Request) -> BaseResponse:
        try:
            version: VersionModel = self._service.get_version()

            content = BaseContent(rc=ResponseCode.OK, data=version)
            return BaseResponse(status_code=st.HTTP_200_OK, content=content)

        except Exception as e:
            self.return_exception(e)

    def home(self, request: Request) -> RedirectResponse:
        # Redirect to Swagger docs
        return RedirectResponse(url="/docs")

    def _create_service(self) -> UtilsService:
        return UtilsService()
