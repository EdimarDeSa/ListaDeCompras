from os import getenv

from app.Routers.auth_router import AuthRoutes
from app.Routers.base_router import BaseRoutes
from app.Routers.user_router import UserRoutes

__all__ = [
    "origins",
    "routers",
    "DEBUG",
]


origins: list[str] = ["*"]


routers: list[type[BaseRoutes]] = [
    AuthRoutes,
    UserRoutes,
    # UnityTypeRouter,
    # DefaultCategoryRouter,
]


DEBUG: bool = bool(int(getenv("DEBUG", "0")))
