from typing import Optional, Annotated

from fastapi import Request, status as st, Depends

from DataBase.models.dto_models import NewUser, UpdateUserDTO, UserDTO, UpdateUserEmailDTO, UpdateUserPasswordDTO
from DataBase.models.token_model import TokenData
from Enums.enums import ResponseCode, LangEnum
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

        # PUT
        self.api_router.add_api_route("/", self.put_user, methods=["PUT"])
        self.api_router.add_api_route("/email/{user_email}", self.put_user_email, methods=["PUT"])
        self.api_router.add_api_route("/password/{user_password}", self.put_user_password, methods=["PUT"])

        # DELETE
        self.api_router.add_api_route("/{user_email}", self.delete_user_when_logged, methods=["DELETE"])

    async def get_me(
        self,
        request: Request,
        current_user: Annotated[TokenData, Depends(decode_token)],
    ) -> BaseResponse:
        self._logger.info("Starting get_me")
        service = self._create_service()

        try:
            self._logger.debug("Starting read_by_id")
            user_dto = service.read_by_id(current_user.id, current_user.language)

            self._logger.info("Retrieving user successfully")
            content = BaseContent(data=user_dto)
            return BaseResponse(status_code=st.HTTP_200_OK, content=content)

        except Exception as e:
            return self.return_exception(e)

    async def post_user(
        self, request: Request, new_user: NewUser, language: Optional[LangEnum] = LangEnum.EN_US
    ) -> BaseResponse:
        service = self._create_service()
        self._logger.info("Starting post_user")

        if request.headers.get("Authorization", None) is not None:
            self._logger.debug("User already logged - Cannot create new user")

            content = BaseContent(rc=ResponseCode.ALREADY_LOGGED)
            return BaseResponse(status_code=st.HTTP_403_FORBIDDEN, content=content)

        try:
            self._logger.debug("Starting create_user")
            user_dto: UserDTO = service.create_user(new_user, language)

            self._logger.info("User successfully created")
            content = BaseContent(data=user_dto)
            return BaseResponse(status_code=st.HTTP_201_CREATED, content=content)

        except Exception as e:
            return self.return_exception(e)

    async def put_user(
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

    async def put_user_email(
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

    async def put_user_password(
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

    async def delete_user_when_logged(
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
