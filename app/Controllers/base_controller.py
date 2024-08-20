from abc import ABC
from typing import Optional

from fastapi import APIRouter

from app.Models.connection import DBConnectionHandler


class BaseController(ABC, APIRouter):
    def __init__(self, prefix: str = ""):
        super().__init__(prefix=prefix)
        self.__db_conn: Optional[DBConnectionHandler] = None

    @property
    def db_conn(self) -> DBConnectionHandler:
        if self.__db_conn is None:
            raise ConnectionError("Database connection is not set.")
        return self.__db_conn

    @db_conn.setter
    def db_conn(self, db_conn: DBConnectionHandler) -> None:
        self.__db_conn = db_conn
