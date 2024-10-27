import logging

from app.conf.app_settings import log_settings, db_settings
from app.conf.db_config import init_db

print("app.__init__.py is running")

# region logger configuration
print("logger configuration")
logging.basicConfig(level=log_settings.LOG_LEVEL,
                    format=log_settings.LOG_FORMAT,
                    handlers=[logging.FileHandler(log_settings.LOG_FILE), logging.StreamHandler()])
logging.getLogger('pymongo').setLevel(logging.INFO)
log = logging.getLogger(__name__)
# endregion logger configuration


print("logger configured")
log.info("PyFAPI Application started")
