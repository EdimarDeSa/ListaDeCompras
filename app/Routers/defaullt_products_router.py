from typing import Annotated

from fastapi import Request, Depends
from fastapi import status as st

from app.DataBase.models.defualt_product_models import NewDefaultProduct
from app.DataBase.models.token_model import TokenData
from app.Enums.enums import LangEnum
from app.Routers.base_router import BaseRoutes
from app.Schemas.responses.base_response import BaseResponse, BaseContent
from app.Services.auth_service import decode_token
from app.Services.default_products_service import DefaultProductsService


class DefaultProductsRoutes(BaseRoutes):
    def __init__(self) -> None:
        self._logger = self.create_logger(__name__)
        self._service = self._create_service()
        self.api_router = self.create_api_router(prefix="/default_products", tags=["Default Products"])
        self.__register_routes()

    def __register_routes(self) -> None:
        # GET
        self.api_router.add_api_route("/all", self.get_all_default_products, methods=["GET"])

        # POST
        self.api_router.add_api_route("/", self.post_new_default_product, methods=["POST"])

    def get_all_default_products(self, request: Request, language: LangEnum) -> BaseResponse:
        service = self._create_service()

        try:
            result = service.get_all_default_products(language)

            content = BaseContent(data=result)
            return BaseResponse(content=content)

        except Exception as e:
            return self.return_exception(e)

    def post_new_default_product(
        self,
        request: Request,
        current_user: Annotated[TokenData, Depends(decode_token)],
        new_product: NewDefaultProduct,
        language: LangEnum,
    ) -> BaseResponse:
        service = self._create_service()

        # TODO: Implementar verificação de perfil
        # if current_user.perfil.name != "ADMIN":
        #     raise InternalErrors.FORBIDDEN_403(ResponseCode.FORBIDDEN_ADMIN_ACCESS, language)

        try:
            result = service.create_new_default_product(new_product, language)

            content = BaseContent(data=result)
            return BaseResponse(status_code=st.HTTP_201_CREATED, content=content)

        except Exception as e:
            return self.return_exception(e)

    def _create_service(self) -> DefaultProductsService:
        return DefaultProductsService()
