import logging

from src.config.logger_config import get_config_logger

settings = get_config_logger()

logging_formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")

logging_handler = logging.FileHandler("logs/app.log")
logging_handler.setFormatter(logging_formatter)


def get_logger(name: str) -> logging.Logger:
    """Get a logger with a given name."""
    if settings.LOG_DISABLE:
        raise Exception("Module Logger is disabled")
    logger: logging.Logger = logging.getLogger(name)
    logger.addHandler(logging_handler)
    logger.setLevel(settings.LOG_LEVEL.upper())

    return logger
