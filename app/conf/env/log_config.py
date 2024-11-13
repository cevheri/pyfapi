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
    LOG_FORMAT: str
        Logging format string for log messages like timestamp, name, level, message
    LOG_HANDLER: list[str]
        Logging handlers like console, file, db
    LOG_BACKUP_COUNT: int 7
        Log file will be rotated after 7 files
    LOG_MAX_DAYS: int 7
        Log file will be rotated after 7 days
    LOG_MAX_SIZE: int 10MB
        Log file will be rotated after 10MB
    """

    LOG_LEVEL: str = "DEBUG"
    LOG_FILE: str = "/tmp/app.log"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_HANDLER: list[str] = ["console", "file", "db"]
    LOG_BACKUP_COUNT: int = 7  # log file will be rotated after 7 files
    LOG_MAX_DAYS: int = 7  # log file will be rotated after 7 days
    LOG_MAX_SIZE: int = (10 * 1024 * 1024)  # 10MB log file will be rotated after 10MB

    class Config:
        # env_prefix = "LOG_"
        env_file = ".env.dev"
        env_file_encoding = "utf-8"
        case_sensitive = True
