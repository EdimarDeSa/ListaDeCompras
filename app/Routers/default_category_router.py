from fastapi import Request

from DataBase.models.dto_models import DefaultCategoryDTO
from Enums.enums import LangEnum
from Routers.base_router import BaseRoutes
from Schemas.responses.base_response import BaseResponse, BaseContent
from Services.default_category_service import DefaultCategoryService


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

        self._logger.info(f"Starting get_all_default_categories")

        try:
            self._logger.debug(f"Getting all default categories")
            default_categories: list[DefaultCategoryDTO] = service.read_all(language)

            self._logger.info(f"Default categories found: {default_categories}")

            content = BaseContent(data=default_categories)
            return BaseResponse(status_code=200, content=content)
        except Exception as e:
            raise self.return_exception(e)

    def _create_service(self) -> DefaultCategoryService:
        return DefaultCategoryService()
