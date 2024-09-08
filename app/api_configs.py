import logging
import os
from logging.handlers import RotatingFileHandler

from starlette.middleware.cors import CORSMiddleware

from app.Middlewares.process_time import add_process_time_header
from app.Routers.auth_router import AuthRoutes
from app.Routers.base_router import BaseRoutes
from app.Routers.defaullt_products_router import DefaultProductsRoutes
from app.Routers.default_category_router import DefaultCategoryRoutes
from app.Routers.unity_type_router import UnityTypeRoutes
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
    UnityTypeRoutes,
    DefaultCategoryRoutes,
    DefaultProductsRoutes,
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
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    logging.basicConfig(level=logging.DEBUG if DEBUG_MODE else logging.WARNING, format=log_format)

    if not logger.handlers:
        log_formater = logging.Formatter(log_format)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formater)
        logger.addHandler(console_handler)

        log_file = os.getenv("LOG_FILE", "app.log")
        rotating_handler = RotatingFileHandler(log_file, maxBytes=2000, backupCount=5)
        rotating_handler.setFormatter(log_formater)
        logger.addHandler(rotating_handler)

    logger.info("Logger activated!")
