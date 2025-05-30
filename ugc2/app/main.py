import contextvars
import logging
from uuid import uuid4

import sentry_sdk
from api.v1 import bookmarks, likes, rates
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
gunicorn_error_logger.addHandler(fastapi_logger)  # type: ignore[arg-type]
gunicorn_access_logger = logging.getLogger("gunicorn.access")
gunicorn_access_logger.addHandler(fastapi_logger)  # type: ignore[arg-type]


if ugc2_settings.sentry_enable:
    sentry_sdk.init(
        dsn=ugc2_settings.sentry_dsn,
        traces_sample_rate=ugc2_settings.sentry_traces_sample_rate,
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

app.include_router(likes.router, prefix="/api/v1/ugc/likes", tags=["like"])
app.include_router(bookmarks.router, prefix="/api/v1/ugc/bookmarks", tags=["bookmark"])
app.include_router(rates.router, prefix="/api/v1/ugc/rates", tags=["rate"])
