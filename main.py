from dotenv import load_dotenv

load_dotenv()

import logging
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.configs import *

logger = logging.getLogger(__name__)


app = FastAPI(
    title="Lista de compras",
    debug=DEBUG_MODE,
    docs_url="/docs",
    contact={"name": "Edimar de Sá", "email": "edimar.sa@efscode.com"},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Registra todos os roteadores listados
for router in routers:
    logger.debug(f"Iniciando - {router.__name__}")
    app.include_router(router().api_router)
