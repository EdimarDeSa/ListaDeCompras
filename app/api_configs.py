import logging
import os
import sys
from logging.handlers import RotatingFileHandler

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from InternalResponse.internal_errors import InternalErrors
from Middlewares.process_time import add_process_time_header
from Routers.auth_router import AuthRoutes
from Routers.base_router import BaseRoutes

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

from Utils.internal_types import METHODS

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
DEBUG_MODE: bool = bool(int(os.getenv("DEBUG_MODE", "0")))

if DEBUG_MODE:
    log_format = (
        "%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s"
    )

    console_handler = logging.StreamHandler(stream=sys.stdout)

    log_file = os.getenv("LOG_FILE", "app.log")
    rotating_handler = RotatingFileHandler(log_file, maxBytes=2000, backupCount=5)

    logging.basicConfig(
        level=logging.DEBUG,
        format=log_format,
        encoding="utf-8",
        handlers=[console_handler, rotating_handler],
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logger = logging.getLogger(__name__)
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
    # UserRoutes,
    # UtilsRoutes,
    # UnityTypeRoutes,
    # DefaultCategoryRoutes,
    # DefaultProductsRoutes,
]


### REGISTER ROUTERS ###
def register_routes(app: FastAPI) -> None:
    for router in routers:
        r = router()

        if not isinstance(r, BaseRoutes):
            raise Exception([InternalErrors.INTERNAL_SERVER_ERROR_500, "Roteador inválido"])

        logger.debug(f"Starting - {r.__class__.__name__}")
        app.include_router(r.api_router)
