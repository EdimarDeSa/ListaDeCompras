from typing import Optional

from app.Enums.enums import LangEnum, HttpMethodsEnum
from app.Enums.http_exceptions import HttpExceptions
from app.Models.dto_models import DefaultCategoryDTO
from app.Routers.base_router import BaseRouter


class DefaultCategoryRouter(BaseRouter):
    def __init__(self) -> None:
        super().__init__(prefix="/default_categorys")
        self.__register_routes()

    def __register_routes(self) -> None:
        # GET
        self.add_api_route("/all", self.get_all_default_categorys, methods=[HttpMethodsEnum.GET])

    async def get_all_default_categorys(self, language: Optional[LangEnum] = None) -> list[DefaultCategoryDTO]:
        default_categorys = self.db_conn.read_all_default_categorys()

        if default_categorys is None:
            raise HttpExceptions.UserNotFound(language)

        return default_categorys
