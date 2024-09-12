from fastapi import status as st, Request
from starlette.responses import RedirectResponse

from DataBase.models.version_model import VersionModel
from Enums.enums import ResponseCode, LangEnum
from InternalResponse.base_internal_response import BaseInternalResponses
from Routers.base_router import BaseRoutes
from Schemas.responses.base_response import BaseResponse, BaseContent
from Services.utils_service import UtilsService


class UtilsRoutes(BaseRoutes):
    def __init__(self):
        self.api_router = self.create_api_router(tags=["Utils"])
        self._logger = self.create_logger(__name__)

        self.register_routes()

    def register_routes(self):
        self._router.add_api_route("/health", self.health, methods=["GET"])
        self._router.add_api_route("/version", self.version, methods=["GET"])
        self._router.add_api_route("/", self.home, methods=["GET"])

    def health(self, request: Request) -> BaseResponse:
        self._logger.info("Checking health...")
        service = self._create_service()

        try:
            result: BaseInternalResponses = service.check_health(LangEnum.EN_US)
            self._logger.info(f"Health check status: {result}")

            content = BaseContent(rc=0, data=result.message)
            return BaseResponse(status_code=200, content=content)

        except Exception as e:
            self.return_exception(e)

    def version(self, request: Request) -> BaseResponse:
        service = self._create_service()
        self._logger.info("Getting version...")

        try:
            version: VersionModel = service.get_version()
            self._logger.debug(f"<Version: {version}>")

            content = BaseContent(rc=ResponseCode.OK, data=version)
            return BaseResponse(status_code=st.HTTP_200_OK, content=content)

        except Exception as e:
            self.return_exception(e)

    def home(self, request: Request) -> RedirectResponse:
        # Redirect to Swagger docs
        self._logger.info("Redirecting from Home to Swagger docs...")
        return RedirectResponse(url="/docs")

    def _create_service(self) -> UtilsService:
        return UtilsService()
