import uuid
from typing import Optional, Annotated

from fastapi import status as st, Depends

from app.Enums.enums import ResponseCode, LangEnum
from app.Models.dto_models import NewUser, UpdateUserDTO, UserDTO
from app.Models.token_model import TokenData
from app.Routers.base_router import BaseRoutes
from app.Schemas.responses.base_response import BaseResponse, BaseContent
from app.Services.auth_service import decode_token
from app.Services.user_service import UserService


class UserRoutes(BaseRoutes):
    def __init__(self) -> None:
        self.router = self.create_api_router(prefix="/users", tags=["Users"])
        self.__register_routes()

    def __register_routes(self) -> None:
        # GET
        self.router.add_api_route("/all", self.get_all_users, methods=["GET"])
        self.router.add_api_route("/me", self.get_me, methods=["GET"])
        self.router.add_api_route("/{user_id}", self.get_user_by_id, methods=["GET"])

        # POST
        self.router.add_api_route("/", self.post_new_user, methods=["POST"])

        # PUT
        self.router.add_api_route("/", self.put_user, methods=["PUT"])

        # DELETE
        self.router.add_api_route("/{user_email}", self.delete_user_by_email, methods=["DELETE"])

    async def get_me(self, current_user: Annotated[TokenData, Depends(decode_token)]) -> BaseResponse:
        service = self._create_service()
        try:
            user_dto = service.read_by_id(current_user.id, current_user.language)

            content = BaseContent(rc=ResponseCode.OK, data=user_dto)
            return BaseResponse(status_code=st.HTTP_200_OK, content=content)

        except Exception as e:
            return self.return_exception(e)

    async def get_all_users(self, language: Optional[LangEnum] = LangEnum.EN) -> BaseResponse:
        service = self._create_service()

        try:
            users_dto = service.read_all(language)

            content = BaseContent(rc=ResponseCode.OK, data=users_dto)
            return BaseResponse(status_code=st.HTTP_200_OK, content=content)

        except Exception as e:
            return self.return_exception(e)

    async def get_user_by_id(self, user_id: uuid.UUID, language: Optional[LangEnum] = LangEnum.EN) -> BaseResponse:
        service = self._create_service()

        try:
            user_dto = service.read_by_id(user_id, language)

            content = BaseContent(rc=ResponseCode.OK, data=user_dto)
            return BaseResponse(status_code=st.HTTP_200_OK, content=content)

        except Exception as e:
            return self.return_exception(e)

    async def post_new_user(self, new_user: NewUser, language: Optional[LangEnum] = LangEnum.EN) -> BaseResponse:
        service = self._create_service()

        try:

            user_dto: UserDTO = service.create_user(new_user, language)

            content = BaseContent(rc=ResponseCode.OK, data=user_dto)
            return BaseResponse(status_code=st.HTTP_201_CREATED, content=content)

        except Exception as e:
            return self.return_exception(e)

    async def put_user(self, update_data: UpdateUserDTO, language: Optional[LangEnum] = LangEnum.EN) -> BaseResponse:
        service = self._create_service()
        try:
            updated_data = service.update_user(update_data, language)

            content = BaseContent(rc=ResponseCode.OK, data=updated_data)
            return BaseResponse(status_code=st.HTTP_202_ACCEPTED, content=content)

        except Exception as e:
            return self.return_exception(e)

    async def delete_user_by_email(self, user_email: str, language: Optional[LangEnum] = LangEnum.EN) -> BaseResponse:
        service = self._create_service()

        try:

            service.delete_user_by_email(user_email)

            content = BaseContent(rc=ResponseCode.OK, data="User deleted")
            return BaseResponse(status_code=st.HTTP_202_ACCEPTED, content=content)

        except Exception as e:
            return self.return_exception(e)

    def _create_service(self) -> UserService:
        return UserService()
