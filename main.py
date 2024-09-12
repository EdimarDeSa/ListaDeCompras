from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI

from api_configs import *


app = FastAPI(
    title=TITLE,
    description=DESCRIPTION,
    debug=DEBUG_MODE,
    docs_url=DOCS_URL,
    contact=CONTACT,
    swagger_ui_parameters=SWAGGER_UI_PARAMETERS,
)

register_middlewares(app)

register_routes(app)
