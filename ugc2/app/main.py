import contextvars
import logging
from uuid import uuid4

import sentry_sdk
from api.v1 import films, users, bookmarks
from core.config import ugc2_settings
from core.logger import fastapi_logger
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse

request_id_context = contextvars.ContextVar("request_id", default=None)


class RequestIDLogFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request_id_context.get()
        return True


gunicorn_error_logger = logging.getLogger("gunicorn.error")
gunicorn_error_logger.addHandler(fastapi_logger)
gunicorn_access_logger = logging.getLogger("gunicorn.access")
gunicorn_access_logger.addHandler(fastapi_logger)


sentry_sdk.init(
    dsn="https://c6e15651de424b3321b89771c9ec00bb@o4508310740598784.ingest.de.sentry.io/4508310743941200",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    _experiments={
        "continuous_profiling_auto_start": True,
    },
)

app = FastAPI(
    title=ugc2_settings.project_name,
    docs_url="/api/v1/ugc/openapi",
    openapi_url="/api/v1/ugc/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.middleware("http")
async def add_request_id_middleware(request: Request, call_next):

    request_id = request.headers.get("x-request-id")

    if not request_id:

        request_id = str(uuid4())

    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-Id"] = request_id
    return response


for handler in fastapi_logger.handlers:
    handler.addFilter(RequestIDLogFilter())

app.include_router(users.router, prefix="/api/v1/ugc")
app.include_router(films.router, prefix="/api/v1/ugc", tags=["film"])
app.include_router(bookmarks.router, prefix="/api/v1/ugc/bookmarks", tags=["bookmark"])
