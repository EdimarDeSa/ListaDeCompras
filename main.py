import time

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.configs import *

load_dotenv()


app = FastAPI(
    title="Lista de compras",
    debug=DEBUG,
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
    app.include_router(router().router)
