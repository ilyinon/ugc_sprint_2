from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import users, films
from core.config import ugc2_settings

app = FastAPI(
    title=ugc2_settings.project_name,
    docs_url="/api/v1/ugc/openapi",
    openapi_url="/api/v1/ugc/openapi.json",
    default_response_class=ORJSONResponse,
)


app.include_router(users.router, prefix="/api/v1")
# app.include_router(films.router, prefix="/api/v1")
