import logging
import logging.handlers

from fastapi.logger import logger as fastapi_logger

logging.basicConfig(
    filename="logs/fastapi.log",  # Log file name
    level=logging.INFO,  # Set minimum logging level
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    datefmt="%Y-%m-%d %H:%M:%S",
)


handler = logging.FileHandler("logs/fastapi.log")  # Use the same file
handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)  # Same log format

console = logging.StreamHandler()
console.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)  # Same log format


fastapi_logger.addHandler(handler)
fastapi_logger.addHandler(console)
