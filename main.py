from os import getenv

from dotenv import load_dotenv
from fastapi import FastAPI

from app.Routers.base_router import BaseRouter
from app.Routers.user_router import UserRouter

load_dotenv()

routers: list[type[BaseRouter]] = [
    UserRouter,
    # UnityTypeRouter,
    # DefaultCategoryRouter,
]

DEBUG: bool = bool(int(getenv("DEBUG", "0")))

app = FastAPI(title="Lista de compras", debug=DEBUG, docs_url="/docs")


for router in routers:
    app.include_router(router())
