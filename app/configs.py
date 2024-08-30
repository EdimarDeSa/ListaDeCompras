import logging
import os
from logging.handlers import RotatingFileHandler

from app.Routers.auth_router import AuthRoutes
from app.Routers.base_router import BaseRoutes
from app.Routers.user_router import UserRoutes

__all__ = [
    "origins",
    "routers",
    "DEBUG_MODE",
]


origins: list[str] = ["*"]


routers: list[type[BaseRoutes]] = [
    AuthRoutes,
    UserRoutes,
    # UnityTypeRouter,
    # DefaultCategoryRouter,
]


DEBUG_MODE: bool = bool(int(os.getenv("DEBUG_MODE", "0")))

log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

logging.basicConfig(level=logging.DEBUG if DEBUG_MODE else logging.WARNING, format=log_format)

logger = logging.getLogger(__name__)


if DEBUG_MODE:
    log_file = os.getenv("LOG_FILE", "app.log")

    rotating_handler = RotatingFileHandler(log_file, maxBytes=2000, backupCount=5)
    rotating_handler.setFormatter(logging.Formatter(log_format))

    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(log_format))

        logger.addHandler(console_handler)
        logger.addHandler(rotating_handler)

    logger.info("Logger configured")
