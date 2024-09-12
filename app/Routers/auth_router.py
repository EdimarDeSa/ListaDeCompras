from typing import Annotated, Optional

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordRequestForm

from DataBase.models.token_model import Token
from Enums.enums import LangEnum, ResponseCode
from InternalResponse.internal_errors import InternalErrors
from Routers.base_router import BaseRoutes
from Schemas.responses.base_response import BaseResponse
from Services.auth_service import AuthService


class AuthRoutes(BaseRoutes):
    def __init__(self) -> None:
        self._logger = self.create_logger(__name__)
        self.api_router = self.create_api_router(tags=["Auth"], prefix="/token")

        self.__register_routes()

    def __register_routes(self) -> None:
        # POST
        self.api_router.add_api_route("", self.login, methods=["POST"])
        self.api_router.add_api_route("/refresh", self.refresh_token, methods=["POST"])

    async def login(
        self,
        request: Request,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        language: Optional[LangEnum] = LangEnum.EN_US,
    ) -> Token or BaseResponse:
        """
        Create a new token for the user.

        Attributes:

            form_data (Annotated[OAuth2PasswordRequestForm, Depends()]): As credenciais fornecidas pelo usuário.
            language (Optional[LangEnum]): Idioma da resposta. Defaults to LangEnum.EN_US.

        Example:

            $ curl -X POST \\
            --url http://localhost:8080/token \\
            --header 'Content-Type: multipart/form-data' \\
            --form username={email@domain.com} \\
            --form password={P@s5W0rd}

            response:
                {
                    "access_token": "{JWT_TOKEN}",
                    "token_type": "bearer"
                }
        """
        self._logger.info("Starting login")

        user_email = form_data.username
        password = form_data.password
        service = self._create_service()

        try:
            self._logger.debug(f"Try login with <Email: {user_email}>")
            token_: Token = service.authenticate_user(user_email=user_email, password=password, language=language)
            self._logger.info(f"Success login - token created")

            return token_

        except Exception as e:
            return self.return_exception(e, headers={"WWW-Authenticate": "Bearer"}, logger=self._logger)

    async def refresh_token(
        self,
        request: Request,
        language: Optional[LangEnum] = LangEnum.EN_US,
    ) -> Token or BaseResponse:
        """
        Atualiza o token JWT se o token de atualização fornecido for válido.

        Attributes:

            language (Optional[LangEnum]): Idioma da resposta. Defaults to LangEnum.EN_US.

        Examples:

            $ curl -X POST \\
            --url http://localhost:8080/token/refresh \\
            --header 'Authorization: Bearer {JWT_TOKEN}'

            response:
                {
                    "access_token": "JWT_TOKEN",
                    "token_type": "bearer"
                }
        """
        service = self._create_service()

        try:
            self._logger.info("Starting refresh_token")

            current_token = request.headers.get("Authorization")
            self._logger.debug(f"Token to refresh: {current_token}")

            if not current_token:
                self._logger.warning("Token to refresh can't be empty")
                raise InternalErrors.FORBIDDEN_403(ResponseCode.INVALID_CREDENTIALS, language)

            current_token_cleaned: str = current_token.split(" ")[1]
            self._logger.debug(f"Token found: {current_token_cleaned}")

            self._logger.debug(f"Refreshing token")
            new_token: Token = service.refresh_jwt_token(current_token_cleaned, language)
            self._logger.info(f"Success refreshing token - created new token")

            return new_token

        except Exception as e:
            return self.return_exception(e, headers={"WWW-Authenticate": "Bearer"}, logger=self._logger)

    def _create_service(self) -> AuthService:
        return AuthService()
