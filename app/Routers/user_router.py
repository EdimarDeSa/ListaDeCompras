from typing import Optional, Annotated

from fastapi import Request, status as st, Depends

from app.DataBase.models.dto_models import NewUser, UpdateUserDTO, UserDTO
from app.DataBase.models.token_model import TokenData
from app.Enums.enums import ResponseCode, LangEnum
from app.Routers.base_router import BaseRoutes
from app.Schemas.responses.base_response import BaseResponse, BaseContent
from app.Services.auth_service import decode_token
from app.Services.user_service import UserService


class UserRoutes(BaseRoutes):
    def __init__(self) -> None:
        self.api_router = self.create_api_router(prefix="/users", tags=["Users"])
        self.__register_routes()

    def __register_routes(self) -> None:
        # GET
        # self.api_router.add_api_route("/all", self.get_all_users, methods=["GET"])
        self.api_router.add_api_route("/me", self.get_me, methods=["GET"])
        # self.api_router.add_api_route("/{user_id}", self.get_user_by_id, methods=["GET"])

        # POST
        self.api_router.add_api_route("/", self.post_new_user, methods=["POST"])

        # PUT
        self.api_router.add_api_route("/", self.put_user, methods=["PUT"])

        # DELETE
        self.api_router.add_api_route("/{user_email}", self.delete_user_when_logged, methods=["DELETE"])

    async def get_me(self, request: Request, current_user: Annotated[TokenData, Depends(decode_token)]) -> BaseResponse:
        service = self._create_service()
        try:
            user_dto = service.read_by_id(current_user.id, current_user.language)

            content = BaseContent(data=user_dto)
            return BaseResponse(status_code=st.HTTP_200_OK, content=content)

        except Exception as e:
            return self.return_exception(e)

    async def get_all_users(self, request: Request, language: Optional[LangEnum] = LangEnum.EN) -> BaseResponse:
        service = self._create_service()

        try:
            users_dto = service.read_all(language)

            content = BaseContent(data=users_dto)
            return BaseResponse(status_code=st.HTTP_200_OK, content=content)

        except Exception as e:
            return self.return_exception(e)

    async def post_new_user(
        self, request: Request, new_user: NewUser, language: Optional[LangEnum] = LangEnum.EN
    ) -> BaseResponse:
        service = self._create_service()

        if request.headers["Authorization"]:
            content = BaseContent(rc=ResponseCode.ALREADY_LOGGED)
            return BaseResponse(status_code=st.HTTP_403_FORBIDDEN, content=content)

        try:

            user_dto: UserDTO = service.create_user(new_user, language)

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
        try:
            user_id = current_user.id
            language = current_user.language
            updated_data = service.update_user(user_id, update_data, language)

            content = BaseContent(data=updated_data)
            return BaseResponse(status_code=st.HTTP_202_ACCEPTED, content=content)

        except Exception as e:
            return self.return_exception(e)

    async def delete_user_when_logged(
        self,
        request: Request,
        current_user: Annotated[TokenData, Depends(decode_token)],
    ) -> BaseResponse:
        service = self._create_service()
        user_id = current_user.id

        try:

            service.delete_user_by_id(user_id, current_user.language)

            content = BaseContent(data="User deleted")
            return BaseResponse(status_code=st.HTTP_202_ACCEPTED, content=content)

        except Exception as e:
            return self.return_exception(e)

    def _create_service(self) -> UserService:
        return UserService()
