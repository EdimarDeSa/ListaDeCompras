import uuid
from typing import Optional

from fastapi import Response

from app.Controllers.base_controller import BaseController
from app.Enums.enums import LangEnum, HttpMethodsEnum
from app.Enums.http_exceptions import HttpExceptions
from app.Enums.http_responses import HttpResponses
from app.Models.connection import DBConnectionHandler
from app.Models.dto_models import UserDTO, NewUser


class UserController(BaseController):
    def __init__(self, db_conn: DBConnectionHandler) -> None:
        super().__init__(prefix="/users")
        self.db_conn = db_conn
        self.__register_routes()

    def __register_routes(self) -> None:
        # GET
        self.add_api_route("/all", self.get_all_users, methods=[HttpMethodsEnum.GET])
        self.add_api_route("/{user_id}", self.get_user_by_id, methods=[HttpMethodsEnum.GET])

        # POST
        self.add_api_route("/", self.post_new_user, methods=[HttpMethodsEnum.POST])

        # PUT
        self.add_api_route("/", self.put_user, methods=[HttpMethodsEnum.PUT])

        # DELETE
        self.add_api_route("/{user_email}", self.delete_user_by_email, methods=[HttpMethodsEnum.DELETE])

    async def get_all_users(self, language: Optional[LangEnum] = None) -> list[UserDTO]:
        users = self.db_conn.read_all_users()

        if users is None:
            raise HttpExceptions.UserNotFound(language)

        return users

    async def get_user_by_id(self, user_id: uuid.UUID, language: Optional[LangEnum] = None) -> UserDTO:
        user = self.db_conn.read_user_by_id(user_id)

        if user is None:
            raise HttpExceptions.UserNotFound(language)

        return user

    async def post_new_user(self, new_user: NewUser, language: Optional[LangEnum] = None) -> Response:
        user = self.db_conn.read_user_by_id(new_user.id)

        if user:
            raise HttpExceptions.UserEmailUsed(language)

        self.db_conn.create_user(new_user)
        return HttpResponses.Created()

    async def put_user(self, user_dto: UserDTO, language: Optional[LangEnum] = None) -> Response:
        user = self.db_conn.read_user_by_id(user_dto.id)

        if user is None:
            raise HttpExceptions.UserNotFound(language)

        self.db_conn.update_user(user_dto)
        return HttpResponses.NoContent()

    async def delete_user_by_email(self, user_email: str, language: Optional[LangEnum] = None) -> Response:
        resp = self.db_conn.delete_user_by_email(user_email)

        if resp is None:
            raise HttpExceptions.UserNotFound(language)

        return HttpResponses.NoContent()
