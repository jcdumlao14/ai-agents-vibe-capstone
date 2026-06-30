import logging
from .settings import settings


def configure_logger() -> logging.Logger:
    logging.basicConfig(level=settings.log_level, format=settings.log_format)
    logger = logging.getLogger(settings.app_name)
    return logger

logger = configure_logger()
