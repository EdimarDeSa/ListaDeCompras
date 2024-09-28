from dotenv import load_dotenv

load_dotenv()

from api_configs import (
    CONTACT,
    DEBUG_MODE,
    DESCRIPTION,
    DOCS_URL,
    SWAGGER_UI_PARAMETERS,
    TITLE,
    register_middlewares,
    register_routes,
)
from fastapi import FastAPI

app = FastAPI(
    title=TITLE,
    description=DESCRIPTION,
    debug=DEBUG_MODE,
    docs_url=DOCS_URL,
    contact=CONTACT,
    swagger_ui_parameters=SWAGGER_UI_PARAMETERS,
)

# register_middlewares(app)

# register_routes(app)
