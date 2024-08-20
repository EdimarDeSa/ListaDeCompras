from os import getenv

from dotenv import load_dotenv
from fastapi import FastAPI

from app.Controllers.default_category_controller import DefaultCategoryController
from app.Controllers.unity_type_controller import UnityTypeController
from app.Controllers.user_controller import UserController
from app.Models.connection import DBConnectionHandler

load_dotenv()

DEBUG = bool(int(getenv("DEBUG", "0")))
DB_DIALECT = getenv("DB_DIALECT", "postgresql")
DB_USER = getenv("DB_USER", "postgres")
DB_PASSWORD = getenv("DB_PASSWORD", "postgres")
DB_IP = getenv("DB_IP", "localhost")
DB_PORT = getenv("DB_PORT", "5432")
DB_NAME = getenv("DB_NAME", "postgres")

SQLALCHEMY_DATABASE_URL = f"{DB_DIALECT}://{DB_USER}:{DB_PASSWORD}@{DB_IP}:{DB_PORT}/{DB_NAME}"

app = FastAPI(title="Lista de compras", debug=DEBUG)
db_conn = DBConnectionHandler(SQLALCHEMY_DATABASE_URL)

controllers = list()

controllers.append(UserController(db_conn))
controllers.append(UnityTypeController(db_conn))
controllers.append(DefaultCategoryController(db_conn))

for controller in controllers:
    app.include_router(controller)


if __name__ == "__main__":
    import uvicorn

    if DEBUG:
        users = db_conn.read_all_users()
        if not users:
            from RawSQL.populate import Populate

            Populate(SQLALCHEMY_DATABASE_URL)

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["app"],
    )
