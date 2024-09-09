from fastapi import Request

from app.Enums.enums import LangEnum
from app.Routers.base_router import BaseRoutes
from app.Schemas.responses.base_response import BaseResponse, BaseContent
from app.Services.unity_type_service import UnityTypeService


class UnityTypeRoutes(BaseRoutes):
    def __init__(self) -> None:
        self._logger = self.create_logger(__name__)
        self.api_router = self.create_api_router(prefix="/unity_types", tags=["Unity type"])

        self.__register_routes()

    def __register_routes(self) -> None:
        # GET
        self.api_router.add_api_route("/all", self.get_all_unity_types, methods=["GET"])
        self.api_router.add_api_route("/name/{unity_type_name}", self.get_unity_type_by_name, methods=["GET"])

    async def get_all_unity_types(self, request: Request, language: LangEnum) -> BaseResponse:
        service = self._create_service()
        self._logger.info("Starting get_all_unity_types")

        try:
            self._logger.debug("Trying to get all unity types")
            unity_types = service.read_all(language=language)
            self._logger.info(f"Unity types found: {unity_types}")

            content = BaseContent(data=unity_types)
            return BaseResponse(content=content)

        except Exception as e:
            return self.return_exception(e)

    async def get_unity_type_by_name(self, request: Request, unity_type_name: str, language: LangEnum) -> BaseResponse:
        service = self._create_service()
        self._logger.info("Starting get_unity_type_by_name")

        try:
            self._logger.debug(f"Trying to get unity type by name: {unity_type_name}")
            unity_type = service.read_by_name(unity_type_name, language)
            self._logger.info(f"Unity type found: {unity_type}")

            content = BaseContent(data=unity_type)
            return BaseResponse(content=content)

        except Exception as e:
            return self.return_exception(e)

    def _create_service(self) -> UnityTypeService:
        return UnityTypeService()
