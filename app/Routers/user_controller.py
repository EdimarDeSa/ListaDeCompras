from typing import Optional
from uuid import UUID

from fastapi import status as st

from app.Enums.enums import HttpMethodsEnum, ResponseCode, LangEnum
from app.Enums.http_exceptions import BaseInternalException
from app.Routers.base_router import BaseRouter
from app.Schemas.responses.base_response import BaseResponse, BaseContent
from app.Services.user_service import UserService


class UserRouter(BaseRouter):
    def __init__(self) -> None:
        super().__init__(prefix="/users", tags=["Users"])
        self.__register_routes()

    def __register_routes(self) -> None:
        # GET
        self.add_api_route("/all", self.get_all_users, methods=[HttpMethodsEnum.GET])
        self.add_api_route("/{user_id}", self.get_user_by_id, methods=[HttpMethodsEnum.GET])

        # POST
        # self.add_api_route("/", self.post_new_user, methods=[HttpMethodsEnum.POST])

        # PUT
        # self.add_api_route("/", self.put_user, methods=[HttpMethodsEnum.PUT])

        # DELETE
        # self.add_api_route("/{user_email}", self.delete_user_by_email, methods=[HttpMethodsEnum.DELETE])

    async def get_all_users(self, language: Optional[LangEnum] = None) -> BaseResponse:
        service = self.create_service()

        try:
            users = service.read_all(language)

            content = BaseContent(rc=ResponseCode.OK, data=users)
            return BaseResponse(status_code=st.HTTP_200_OK, content=content)

        except:
            content = BaseContent(rc=ResponseCode.UNKNOWN_ERROR)
            return BaseResponse(status_code=st.HTTP_500_INTERNAL_SERVER_ERROR, content=content)

    async def get_user_by_id(self, user_id: UUID, language: Optional[LangEnum] = None) -> BaseResponse:
        service = self.create_service()

        try:
            user = service.read_by_id(user_id, language)

            content = BaseContent(rc=ResponseCode.OK, data=user)
            return BaseResponse(status_code=st.HTTP_200_OK, content=content)

        except Exception as e:

            if isinstance(e, BaseInternalException):
                content = BaseContent(rc=e.rc, data=e.message)
                return BaseResponse(status_code=e.status_code, content=content)

            content = BaseContent(rc=ResponseCode.UNKNOWN_ERROR)
            return BaseResponse(status_code=st.HTTP_500_INTERNAL_SERVER_ERROR, content=content)

    # async def post_new_user(self, new_user: NewUser, language: Optional[LangEnum] = None) -> Response:
    #     user = self.db_conn.read_user_by_id(new_user.id)
    #
    #     if user:
    #         raise HttpExceptions.UserEmailUsed(language)
    #
    #     self.db_conn.create_user(new_user)
    #     return HttpResponses.Created()
    #
    # async def put_user(self, user_dto: UserDTO, language: Optional[LangEnum] = None) -> Response:
    #     user = self.db_conn.read_user_by_id(user_dto.id)
    #
    #     if user is None:
    #         raise HttpExceptions.UserNotFound(language)
    #
    #     self.db_conn.update_user(user_dto)
    #     return HttpResponses.NoContent()
    #
    # async def delete_user_by_email(self, user_email: str, language: Optional[LangEnum] = None) -> Response:
    #     resp = self.db_conn.delete_user_by_email(user_email)
    #
    #     if resp is None:
    #         raise HttpExceptions.UserNotFound(language)
    #
    #     return HttpResponses.NoContent()

    def create_service(self) -> UserService:
        return UserService()
