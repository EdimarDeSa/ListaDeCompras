from dotenv import load_dotenv

load_dotenv()

import logging

from fastapi import FastAPI

from app.configs import *

logger = logging.getLogger(__name__)


app = FastAPI(
    title="Mundo de compras",
    debug=DEBUG_MODE,
    docs_url="/docs",
    contact={"name": "Edimar de Sá", "email": "edimar.sa@efscode.com"},
)


# Registra todos os middlewares listados
for middleware in middlewares:
    if "http" in middleware.get("options", False):
        app.middleware("http")(middleware["middleware_class"])
    else:
        app.add_middleware(middleware["middleware_class"], **middleware["options"])


# Registra todos os roteadores listados
for router in routers:
    r = router()
    logger.debug(f"Iniciando - {r.__class__.__name__}")
    app.include_router(r.api_router)
