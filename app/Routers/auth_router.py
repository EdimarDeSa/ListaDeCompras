import logging
from typing import Annotated, Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.Enums.enums import LangEnum
from app.Models.token_model import Token
from app.Routers.base_router import BaseRoutes
from app.Schemas.responses.base_response import BaseResponse
from app.Services.auth_service import AuthService


class AuthRoutes(BaseRoutes):
    def __init__(self) -> None:
        self._service = self._create_service()
        self.router = self.create_api_router(tags=["Auth"])

        self.__register_routes()

    def __register_routes(self) -> None:
        # POST
        self.router.add_api_route("/token", self.login, methods=["POST"])

    async def login(
        self, form_data: Annotated[OAuth2PasswordRequestForm, Depends()], language: Optional[LangEnum] = LangEnum.EN
    ) -> Token or BaseResponse:
        user_email = form_data.username
        password = form_data.password
        try:
            token_: Token = self._service.authenticate_user(user_email=user_email, password=password, language=language)
            return token_

        except Exception as e:
            logging.getLogger(__name__).exception(e)
            return self.return_exception(e)

    def _create_service(self) -> AuthService:
        return AuthService()
