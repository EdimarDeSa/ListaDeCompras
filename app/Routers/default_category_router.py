from fastapi import Request

from app.Enums.enums import LangEnum
from app.Routers.base_router import BaseRoutes
from app.Schemas.responses.base_response import BaseResponse, BaseContent
from app.Services.default_category_service import DefaultCategoryService


class HttpExceptions:
    pass


class DefaultCategoryRoutes(BaseRoutes):
    def __init__(self) -> None:
        self._logger = self.create_logger(__name__)
        self.api_router = self.create_api_router(prefix="/default_category", tags=["Default category"])

        self.__register_routes()

    def __register_routes(self) -> None:
        # GET
        self.api_router.add_api_route("/all", self.get_all_default_categories, methods=["GET"])

    async def get_all_default_categories(self, request: Request, language: LangEnum) -> BaseResponse:
        service = self._create_service()

        try:
            default_categories = service.read_all(language)

            content = BaseContent(data=default_categories)
            return BaseResponse(status_code=200, content=content)
        except Exception as e:
            raise self.return_exception(e)

    def _create_service(self) -> DefaultCategoryService:
        return DefaultCategoryService()
