import logging
import os
from logging.handlers import RotatingFileHandler

from starlette.middleware.cors import CORSMiddleware

from app.Middlewares.process_time import add_process_time_header
from app.Routers.auth_router import AuthRoutes
from app.Routers.base_router import BaseRoutes
from app.Routers.user_router import UserRoutes
from app.Routers.utils_router import UtilsRoutes

__all__ = [
    "routers",
    "DEBUG_MODE",
    "middlewares",
]


routers: list[type[BaseRoutes]] = [
    AuthRoutes,
    UserRoutes,
    UtilsRoutes,
    # UnityTypeRouter,
    # DefaultCategoryRouter,
]


origins: list[str] = ["*"]


middlewares = [
    {
        "middleware_class": CORSMiddleware,
        "options": {
            "allow_origins": origins,
            "allow_credentials": True,
            "allow_methods": ["*"],
            "allow_headers": ["*"],
        },
    },
    {"middleware_class": add_process_time_header, "options": {"http": True}},
]


DEBUG_MODE: bool = bool(int(os.getenv("DEBUG_MODE", "0")))


logger = logging.getLogger(__name__)


if DEBUG_MODE:
    log_file = os.getenv("LOG_FILE", "app.log")
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    logging.basicConfig(level=logging.DEBUG if DEBUG_MODE else logging.WARNING, format=log_format)

    rotating_handler = RotatingFileHandler(log_file, maxBytes=2000, backupCount=5)
    rotating_handler.setFormatter(logging.Formatter(log_format))

    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(log_format))

        logger.addHandler(console_handler)
        logger.addHandler(rotating_handler)

    logger.info("Logger configured")
