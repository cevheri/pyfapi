import logging as log
from app.config.app_settings import log_settings, db_settings
from app.config.db_config import load_database_settings

print("APP - LOG_LEVEL:", log_settings.LOG_LEVEL)
print("APP - LOG_FILE:", log_settings.LOG_FILE)
print("APP - LOG_FORMAT:", log_settings.LOG_FORMAT)

log.basicConfig(level=log_settings.LOG_LEVEL,
                format=log_settings.LOG_FORMAT,
                handlers=[log.FileHandler(log_settings.LOG_FILE),log.StreamHandler()])

log = log.getLogger(__name__)
load_database_settings()
log.info("PyFAPI Application started")