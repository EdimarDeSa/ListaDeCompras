import uuid
from typing import Optional

from app.Enums.enums import LangEnum, HttpMethodsEnum
from app.Enums.http_exceptions import HttpExceptions
from app.Models.dto_models import UnityTypeDTO
from app.Routers.base_router import BaseRouter


class UnityTypeRouter(BaseRouter):
    def __init__(self) -> None:
        super().__init__(prefix="/unity_types")
        self.__register_routes()

    def __register_routes(self) -> None:
        # GET
        self.add_api_route("/all", self.get_all_unity_types, methods=[HttpMethodsEnum.GET])
        self.add_api_route("/1/{unity_type_id}", self.get_unity_type_by_id, methods=[HttpMethodsEnum.GET])
        self.add_api_route("/name/{unity_type_name}", self.get_unity_type_by_name, methods=[HttpMethodsEnum.GET])

    async def get_all_unity_types(self, language: Optional[LangEnum] = None) -> list[UnityTypeDTO]:
        unity_types = self.db_conn.read_all_unity_types()

        if unity_types is None:
            raise HttpExceptions.UserNotFound(language)

        return unity_types

    async def get_unity_type_by_id(self, unity_type_id: uuid.UUID, language: Optional[LangEnum] = None) -> UnityTypeDTO:
        unity_type = self.db_conn.read_unity_type_by_id(unity_type_id)

        if unity_type is None:
            raise HttpExceptions.UserNotFound(language)

        return unity_type

    async def get_unity_type_by_name(self, unity_type_name: str, language: Optional[LangEnum] = None) -> UnityTypeDTO:
        unity_type = self.db_conn.read_unity_type_by_name(unity_type_name)

        if unity_type is None:
            raise HttpExceptions.UserNotFound(language)

        return unity_type
