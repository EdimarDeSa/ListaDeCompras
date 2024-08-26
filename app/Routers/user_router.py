import uuid
from typing import Optional

from fastapi import status as st

from app.Enums.enums import ResponseCode, LangEnum
from app.Models.dto_models import NewUser, UpdateUserDTO
from app.Routers.base_router import BaseRouter
from app.Schemas.responses.base_response import BaseResponse, BaseContent
from app.Services.user_service import UserService


class UserRouter(BaseRouter):
    def __init__(self) -> None:
        super().__init__(prefix="/users", tags=["Users"])
        self.__register_routes()

    def __register_routes(self) -> None:
        # GET
        self.add_api_route("/all", self.get_all_users, methods=["GET"])
        self.add_api_route("/{user_id}", self.get_user_by_id, methods=["GET"])

        # POST
        self.add_api_route("/", self.post_new_user, methods=["POST"])

        # PUT
        self.add_api_route("/", self.put_user, methods=["PUT"])

        # DELETE
        # self.add_api_route("/{user_email}", self.delete_user_by_email, methods=["DELETE"])

    async def get_all_users(self, language: Optional[LangEnum] = LangEnum.EN) -> BaseResponse:
        service = self.create_service()

        try:
            users_dto = service.read_all(language)

            content = BaseContent(rc=ResponseCode.OK, data=users_dto)
            return BaseResponse(status_code=st.HTTP_200_OK, content=content)

        except Exception as e:
            return self.return_exception(e)

    async def get_user_by_id(self, user_id: uuid.UUID, language: Optional[LangEnum] = LangEnum.EN) -> BaseResponse:
        service = self.create_service()

        try:
            user_dto = service.read_by_id(user_id, language)

            content = BaseContent(rc=ResponseCode.OK, data=user_dto)
            return BaseResponse(status_code=st.HTTP_200_OK, content=content)

        except Exception as e:
            return self.return_exception(e)

    async def post_new_user(self, new_user: NewUser, language: Optional[LangEnum] = LangEnum.EN) -> BaseResponse:
        service = self.create_service()

        try:

            user_dto = service.create_user(new_user, language)

            content = BaseContent(rc=ResponseCode.OK, data=user_dto)
            return BaseResponse(status_code=st.HTTP_201_CREATED, content=content)

        except Exception as e:
            return self.return_exception(e)

    async def put_user(self, update_data: UpdateUserDTO, language: Optional[LangEnum] = LangEnum.EN) -> BaseResponse:
        service = self.create_service()
        try:
            updated_data = service.update_user(update_data, language)

            content = BaseContent(rc=ResponseCode.OK, data=updated_data)
            return BaseResponse(status_code=st.HTTP_202_ACCEPTED, content=content)

        except Exception as e:
            return self.return_exception(e)

    # async def delete_user_by_email(self, user_email: str, language: Optional[LangEnum] = None) -> Response:
    #     resp = self.db_conn.delete_user_by_email(user_email)
    #
    #     if resp is None:
    #         raise HttpExceptions.UserNotFound(language)
    #
    #     return HttpResponses.NoContent()

    def create_service(self) -> UserService:
        return UserService()
