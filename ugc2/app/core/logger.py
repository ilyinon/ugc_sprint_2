import contextvars
import logging
import logging.handlers

from fastapi.logger import logger as fastapi_logger

request_id_context = contextvars.ContextVar("request_id", default=None)

LOG_FORMAT = '{"request_id": "%(request_id)s", "asctime": \
             "%(asctime)s", "levelname": "%(levelname)s", \
             "name": "%(name)s", "message": "%(message)s"}'


class RequestIDLogFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request_id_context.get()
        return True


logging.basicConfig(
    filename="logs/fastapi.log",  # Log file name
    level=logging.INFO,  # Set minimum logging level
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    datefmt="%Y-%m-%d %H:%M:%S",
)


handler = logging.FileHandler("logs/fastapi.log")  # Use the same file
handler.setFormatter(logging.Formatter(LOG_FORMAT))

console = logging.StreamHandler()
console.setFormatter(logging.Formatter(LOG_FORMAT))


fastapi_logger.addHandler(handler)
fastapi_logger.addHandler(console)
fastapi_logger.addFilter(RequestIDLogFilter())
