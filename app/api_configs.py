import logging
import os
from logging.handlers import RotatingFileHandler

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.InternalResponse.internal_errors import InternalErrors
from app.Middlewares.process_time import add_process_time_header
from app.Routers.auth_router import AuthRoutes
from app.Routers.base_router import BaseRoutes
from app.Routers.defaullt_products_router import DefaultProductsRoutes
from app.Routers.default_category_router import DefaultCategoryRoutes
from app.Routers.unity_type_router import UnityTypeRoutes
from app.Routers.user_router import UserRoutes
from app.Routers.utils_router import UtilsRoutes

__all__ = [
    "TITLE",
    "DESCRIPTION",
    "DOCS_URL",
    "DEBUG_MODE",
    "CONTACT",
    "SWAGGER_UI_PARAMETERS",
    "routers",
    "middlewares",
    "register_middlewares",
    "register_routes",
]

from app.Utils.internal_types import METHODS

### APP CONFIG ###

TITLE = "Mundo de compras"


DESCRIPTION = "Aplicação RestFull de lista de compras"

DOCS_URL = "/docs"

CONTACT = {
    "name": "Edimar de Sá",
    "email": "edimar.sa@efscode.com",
    "url": "https://efscode.com",
}

SWAGGER_UI_PARAMETERS = {
    "docExpansion": "none",
    "deepLinking": False,
    "persistAuthorization": True,
    "displayOperationId": False,
    "displayRequestDuration": True,
    "defaultModelsExpandDepth": 0,
    "filter": True,
    "operationsSorter": "method",
    "requestSnippets": [
        {"lang": "curl", "label": "cURL"},
        {"lang": "python", "label": "Python Requests"},
    ],
    "requestTimeout": 5000,
    "showExtensions": True,
    "showCommonExtensions": True,
    "syntaxHighlight": True,
    "supportedSubmitMethods": METHODS,
    "tryItOutEnabled": False,
    "theme": "flattop",
}


### LOGGER ###
logger = logging.getLogger(__name__)


DEBUG_MODE: bool = bool(int(os.getenv("DEBUG_MODE", "0")))


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


### ORIGINS ###
origins: list[str] = ["*"]


### MIDDLEWARES ###
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


### REGISTER MIDDLEWARES ###
def register_middlewares(app: FastAPI) -> None:
    for middleware in middlewares:
        logger.debug(f"Iniciando - {middleware['middleware_class'].__name__}")

        if "http" in middleware.get("options", False):
            app.middleware("http")(middleware["middleware_class"])
            return

        app.add_middleware(middleware["middleware_class"], **middleware["options"])


### ROUTERS ###
routers: list[type[BaseRoutes]] = [
    AuthRoutes,
    UserRoutes,
    UtilsRoutes,
    UnityTypeRoutes,
    DefaultCategoryRoutes,
    DefaultProductsRoutes,
]


### REGISTER ROUTERS ###
def register_routes(app: FastAPI) -> None:
    for router in routers:
        r = router()

        if not isinstance(r, BaseRoutes):
            raise Exception([InternalErrors.INTERNAL_SERVER_ERROR_500, "Roteador inválido"])

        logger.debug(f"Starting - {r.__class__.__name__}")
        app.include_router(r.api_router)
