# Logging configuration

from pydantic_settings import BaseSettings


class LoggingSettings(BaseSettings):
    """
    Logging settings

    Attributes:
    -----------
    LOG_LEVEL: str
        Logging level
    LOG_FILE: str
        Logging file
    """

    LOG_LEVEL: str = "DEBUG"
    LOG_FILE: str = "/tmp/app.log"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
