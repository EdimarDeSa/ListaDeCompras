from typing import Optional

from fastapi import Request

from DataBase.models.dto_models import UnityTypeDTO
from Enums.enums import LangEnum
from Routers.base_router import BaseRoutes
from Schemas.requests.base_request import BaseRequest
from Schemas.responses.base_response import BaseResponse, BaseContent
from Services.unity_type_service import UnityTypeService


class UnityTypeRoutes(BaseRoutes):
    def __init__(self) -> None:
        self._logger = self.create_logger(__name__)
        self.api_router = self.create_api_router(prefix="/unity_type", tags=["Unity type"])

        self.__register_routes()

    def __register_routes(self) -> None:
        # GET
        self.api_router.add_api_route("/all", self.get_all_unity_types, methods=["GET"])
        self.api_router.add_api_route("/name", self.get_unity_type_by_name, methods=["GET"])

    async def get_all_unity_types(
        self, request: Request, base_request: BaseRequest
    ) -> BaseResponse:
        """
        Get all unity types

        Args:

            language (LangEnum, Optional): Language of the responses. Defaults to 'EN_US'.

        Examples:

            $ curl -X GET \\
            https://localhost:8080/unity_type/all \\
            --data '{"language": "PT_BR"}'

        Returns:

            {
                rc=0,
                data=[
                    {
                        "id": UUID,
                        "name": string,
                        "base_calc": int,
                        "description": string,
                        "creation": datetime,
                        "last_update": datetime
                    },
                    ...,
                    {
                        "id": UUID,
                        "name": string,
                        "base_calc": int,
                        "description": string,
                        "creation": datetime,
                        "last_update": datetime
                    }
                ]
            }
        """

        service = self._create_service()
        self._logger.info("Starting get_all_unity_types")

        print(language)

        try:
            self._logger.debug("Trying to get all unity types")
            unity_types: list[UnityTypeDTO] = service.read_all(language=language)
            self._logger.info(f"Unity types found: {unity_types}")

            content = BaseContent(data=unity_types)
            return BaseResponse(content=content)

        except Exception as e:
            return self.return_exception(e)

    async def get_unity_type_by_name(self, request: Request, name: str, language: LangEnum) -> BaseResponse:
        """
        Get unity type by name

        Args:

            name (str): Name of the unity type
            language:

        Returns:

        """

        service = self._create_service()
        self._logger.info("Starting get_unity_type_by_name")

        try:
            self._logger.debug(f"Trying to get unity type by name: {name}")
            unity_type = service.read_by_name(name, language)
            self._logger.info(f"Unity type found: {unity_type}")

            content = BaseContent(data=unity_type)
            return BaseResponse(content=content)

        except Exception as e:
            return self.return_exception(e)

    def _create_service(self) -> UnityTypeService:
        return UnityTypeService()
