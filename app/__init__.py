import logging as log
from app.config.app_settings import log_settings, db_settings
from app.config.db_config import load_database_settings

print("__init__.py is running")

#region logger configuration
print("logger configuration")
log.basicConfig(level=log_settings.LOG_LEVEL,
                format=log_settings.LOG_FORMAT,
                handlers=[log.FileHandler(log_settings.LOG_FILE),log.StreamHandler()])
log = log.getLogger(__name__)
#endregion logger configuration



print("logging application started")
log.info("PyFAPI Application started")



