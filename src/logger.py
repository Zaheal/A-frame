import os
import logging
from dotenv import load_dotenv

load_dotenv()
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_DISABLE = bool(os.getenv("LOG_DISABLE"))
LOG_PATH = os.getenv("LOG_PATH")

logging_formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")

logging_handler = logging.FileHandler(os.path.join(LOG_PATH, f"{__name__}.log"))
logging_handler.setFormatter(logging_formatter)


def get_logger(name: str) -> logging.Logger:
    """Get a logger with a given name."""
    if LOG_DISABLE:
        raise Exception("Module Logger is disabled")
    logger: logging.Logger = logging.getLogger(name)
    logger.addHandler(logging_handler)
    logger.setLevel(LOG_LEVEL.upper())

    return logger
