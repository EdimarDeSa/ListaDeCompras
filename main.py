from os import getenv

from dotenv import load_dotenv
from fastapi import FastAPI

from app.Routers.base_router import BaseRouter
from app.Routers.user_controller import UserRouter

load_dotenv()

controllers: list[type[BaseRouter]] = [
    UserRouter,
    # UnityTypeRouter,
    # DefaultCategoryRouter,
]

DEBUG: bool = bool(int(getenv("DEBUG", "0")))

app = FastAPI(title="Lista de compras", debug=DEBUG)

for controller in controllers:
    app.include_router(controller())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=DEBUG, reload_dirs=["app"])
