from typing import Optional, Annotated

from fastapi import Request, status as st, Depends

from DataBase.models.dto_models import NewUser, UpdateUserDTO, UserDTO, UpdateUserEmailDTO, UpdateUserPasswordDTO
from DataBase.models.token_model import TokenData
from Enums.enums import ResponseCode, LangEnum
from InternalResponse.base_internal_response import BaseInternalResponses
from InternalResponse.internal_errors import InternalErrors
from Routers.base_router import BaseRoutes
from Schemas.responses.base_response import BaseResponse, BaseContent
from Services.auth_service import decode_token
from Services.user_service import UserService


class UserRoutes(BaseRoutes):
    def __init__(self) -> None:
        self._logger = self.create_logger(__name__)
        self.api_router = self.create_api_router(prefix="/users", tags=["Users"])

        self.__register_routes()

    def __register_routes(self) -> None:
        # GET
        self.api_router.add_api_route("/me", self.get_me, methods=["GET"])

        # POST
        self.api_router.add_api_route("/", self.post_user, methods=["POST"])

        # PATCH
        self.api_router.add_api_route("/update_user", self.patch_user_details, methods=["PATCH"])
        self.api_router.add_api_route("/update_email", self.patch_user_email, methods=["PATCH"])
        self.api_router.add_api_route("/update_password", self.patch_user_password, methods=["PATCH"])

        # DELETE
        self.api_router.add_api_route("/", self.delete_user, methods=["DELETE"])

    async def get_me(
        self,
        request: Request,
        current_user: Annotated[TokenData, Depends(decode_token)],
    ) -> BaseResponse:
        """
        Get self user information

        Examples:
            curl -X GET \\
            --url http://localhost:8080/users/me \\
            --header 'Authorization: Bearer {token}'

            response:
                {
                    "rc": 0,
                    "data": {
                        "name": str,
                        "last_update": date_time_utc,
                        "email": str,
                        "language": LangEnum,
                        "birthdate": date
                    }
                }
        """
        self._logger.info("Starting get_me")
        service = self._create_service()

        try:
            self._logger.debug("Starting read_by_id")
            user_dto = service.read_by_id(current_user.id, current_user.language)

            self._logger.info("Retrieving user successfully")
            content = BaseContent(data=user_dto)
            return BaseResponse(status_code=st.HTTP_200_OK, content=content)

        except Exception as e:
            return self.return_exception(e, logger=self._logger)

    async def post_user(
        self, request: Request, new_user: NewUser, language: Optional[LangEnum] = LangEnum.EN_US
    ) -> BaseResponse:
        """
        Create a new user

        Args:
            new_user (NewUser): new user data
            language (Optional[LangEnum]): language. Defaults to LangEnum.EN_US.

        Examples:
            curl -X POST \\
            --url http://localhost:8080/users \\
            --header 'Content-Type: application/json' \\
            --header 'Authorization: Bearer {token}' \\
            --data '{\\
                      "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",\\
                      "name": "string",\\
                      "creation": "2024-09-12T03:14:36.820Z",\\
                      "last_update": "2024-09-12T03:14:36.820Z",\\
                      "password": "P@s5W0rD",\\
                      "email": "your.email@domain.com",\\
                      "language": "PT_BR",\\
                      "birthdate": "2024-09-12"\\
                    }'

        """
        self._logger.info("Starting post_user")

        service = self._create_service()

        self._logger.debug(f"Checking if user already logged {request.headers}")
        if request.headers.get("Authorization", None) is not None:
            self._logger.warning("User already logged - Cannot create new user")

            internal_error: BaseInternalResponses = InternalErrors.FORBIDDEN_403(
                rc=ResponseCode.ALREADY_LOGGED, language=language
            )

            content = BaseContent(rc=internal_error.rc, data=internal_error.message)
            return BaseResponse(status_code=internal_error.status_code, content=content)

        try:

            self._logger.debug("Starting user creation")
            user_dto: UserDTO = service.create_user(new_user, language)

            self._logger.info("User successfully created")
            content = BaseContent(data=user_dto)
            return BaseResponse(status_code=st.HTTP_201_CREATED, content=content)

        except Exception as e:
            return self.return_exception(e, logger=self._logger)

    async def patch_user_details(
        self,
        request: Request,
        current_user: Annotated[TokenData, Depends(decode_token)],
        update_data: UpdateUserDTO,
    ) -> BaseResponse:
        service = self._create_service()
        self._logger.info("Starting put_user")

        try:

            self._logger.debug("Starting update_user")
            updated_data = service.update_user(current_user.id, update_data, current_user.language)

            self._logger.info("User successfully updated")
            content = BaseContent(data=updated_data)
            return BaseResponse(status_code=st.HTTP_202_ACCEPTED, content=content)

        except Exception as e:
            return self.return_exception(e)

    async def patch_user_email(
        self,
        request: Request,
        current_user: Annotated[TokenData, Depends(decode_token)],
        new_email: UpdateUserEmailDTO,
    ) -> BaseResponse:
        service = self._create_service()
        self._logger.info("Starting put_user_email")

        try:
            self._logger.debug("Starting update_user_email")
            service.update_user_email(current_user.id, new_email, current_user.language)

            self._logger.info("User email successfully updated")
            content = BaseContent(data=new_email)
            return BaseResponse(status_code=st.HTTP_202_ACCEPTED, content=content)

        except Exception as e:
            return self.return_exception(e)

    async def patch_user_password(
        self,
        request: Request,
        current_user: Annotated[TokenData, Depends(decode_token)],
        new_password: UpdateUserPasswordDTO,
    ) -> BaseResponse:
        service = self._create_service()
        self._logger.info("Starting put_user_password")

        try:
            self._logger.debug("Starting update_user_password")
            service.update_user_password(current_user.id, new_password, current_user.language)

            self._logger.info("User password successfully updated")
            content = BaseContent(data="OK")
            return BaseResponse(status_code=st.HTTP_202_ACCEPTED, content=content)

        except Exception as e:
            return self.return_exception(e)

    async def delete_user(
        self,
        request: Request,
        current_user: Annotated[TokenData, Depends(decode_token)],
    ) -> BaseResponse:
        service = self._create_service()
        self._logger.info("Starting delete_user")

        try:

            self._logger.debug("Starting delete_user_by_id")
            service.delete_user_by_id(current_user.id, current_user.language)

            self._logger.info("User successfully deleted")
            content = BaseContent(data="User deleted")
            return BaseResponse(status_code=st.HTTP_202_ACCEPTED, content=content)

        except Exception as e:
            return self.return_exception(e)

    def _create_service(self) -> UserService:
        return UserService()
