import sentry_sdk
from api.v1 import films, users
from core.config import ugc2_settings
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

sentry_sdk.init(
    dsn="https://c6e15651de424b3321b89771c9ec00bb@o4508310740598784.ingest.de.sentry.io/4508310743941200",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    _experiments={
        # Set continuous_profiling_auto_start to True
        # to automatically start the profiler on when
        # possible.
        "continuous_profiling_auto_start": True,
    },
)

app = FastAPI(
    title=ugc2_settings.project_name,
    docs_url="/api/v1/ugc/openapi",
    openapi_url="/api/v1/ugc/openapi.json",
    default_response_class=ORJSONResponse,
)

app.include_router(users.router, prefix="/api/v1")
app.include_router(films.router, prefix="/api/v1")
