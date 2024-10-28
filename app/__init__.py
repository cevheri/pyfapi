import logging

from app.conf.app_settings import log_settings, db_settings
from app.conf.db_config import init_db

print("app.__init__.py is running")

# region logger configuration
print("logger configuration")
logging.basicConfig(level=log_settings.LOG_LEVEL,
                    format=log_settings.LOG_FORMAT,
                    handlers=[logging.FileHandler(log_settings.LOG_FILE), logging.StreamHandler()])
logging.getLogger("pymongo").setLevel(logging.WARN)
logging.getLogger("uvicorn").setLevel(logging.WARN)
logging.getLogger("pydantic").setLevel(logging.WARN)
logging.getLogger("fastapi").setLevel(logging.WARN)
logging.getLogger("beanie").setLevel(logging.WARN)
logging.getLogger("urllib3").setLevel(logging.WARN)
logging.getLogger("passlib").setLevel(logging.WARN)
logging.getLogger("starlette").setLevel(logging.WARN)
logging.getLogger("bitsandbytes").setLevel(logging.WARN)
logging.getLogger("sentence_transformers").setLevel(logging.WARN)
log = logging.getLogger(__name__)
# endregion logger configuration


print("logger configured")
log.info("PyFAPI Application started")
