from typing import Annotated, Optional

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordRequestForm

from app.DataBase.models.token_model import Token
from app.Enums.enums import LangEnum, ResponseCode
from app.InternalResponse.internal_errors import InternalErrors
from app.Routers.base_router import BaseRoutes
from app.Schemas.responses.base_response import BaseResponse
from app.Services.auth_service import AuthService


class AuthRoutes(BaseRoutes):
    def __init__(self) -> None:
        self._logger = self.create_logger(__name__)
        self.api_router = self.create_api_router(tags=["Auth"])

        self.__register_routes()

    def __register_routes(self) -> None:
        # POST
        self.api_router.add_api_route("/token", self.login, methods=["POST"])
        self.api_router.add_api_route(
            "/token/refresh", self.refresh_token, methods=["POST"]
        )  # Nova rota de atualização do token

    async def login(
        self,
        request: Request,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        language: Optional[LangEnum] = LangEnum.EN_US,
    ) -> Token or BaseResponse:
        """
        Cria um novo token JWT para o usuário se as credenciais fornecidas forem válidas.

        Attributes:

            form_data (Annotated[OAuth2PasswordRequestForm, Depends()]): As credenciais fornecidas pelo usuário.
            language (Optional[LangEnum], optional): Idioma da resposta. Defaults to LangEnum.EN_US.

        Raises:

            InternalErrors.UNAUTHORIZED_401: se as credenciais fornecidas forem inválidas.
        """
        user_email = form_data.username
        password = form_data.password
        service = self._create_service()

        try:
            self._logger.info(f"Starting login - {user_email}")
            token_: Token = service.authenticate_user(user_email=user_email, password=password, language=language)
            self._logger.info(f"Success login - created token - {token_.access_token}")
            return token_

        except Exception as e:
            self._logger.exception(e)
            return self.return_exception(e, headers={"WWW-Authenticate": "Bearer"})

    async def refresh_token(
        self, request: Request, language: Optional[LangEnum] = LangEnum.EN_US
    ) -> Token or BaseResponse:
        """
        Atualiza o token JWT se o token de atualização fornecido for válido.

        Attributes:

            language (Optional[LangEnum], optional): Idioma da resposta. Defaults to LangEnum.EN_US.

        Raises:

            InternalErrors.UNAUTHORIZED_401: Se as credenciais fornecidas forem inválidas.
        """
        service = self._create_service()

        try:
            self._logger.info("Starting refresh token")
            refresh_token = request.headers.get("Authorization")
            self._logger.info(f"Refresh token: {refresh_token}")

            if not refresh_token:
                raise InternalErrors.FORBIDDEN_403(ResponseCode.INVALID_CREDENTIALS, language)

            refresh_token = refresh_token.split(" ")[1]
            self._logger.info(f"Refresh token without Bearer: {refresh_token}")

            self._logger.debug(f"Starting refresh token")
            new_token: Token = service.refresh_jwt_token(refresh_token=refresh_token, language=language)
            self._logger.info(f"Success refresh token - created token - {new_token.access_token}")

            return new_token

        except Exception as e:
            self._logger.exception(e)
            return self.return_exception(e, headers={"WWW-Authenticate": "Bearer"})

    def _create_service(self) -> AuthService:
        return AuthService()
