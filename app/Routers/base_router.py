from abc import ABC, abstractmethod

from fastapi import APIRouter

from app.Services.user_service import BaseService


class BaseRouter(ABC, APIRouter):
    @abstractmethod
    def create_service(self) -> type[BaseService]:
        pass
