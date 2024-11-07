import logging

from log4mongo.handlers import MongoHandler

from app.conf.app_settings import log_settings, app_settings, db_settings

def init_log():
    _handlers = [logging.FileHandler(log_settings.LOG_FILE),
                 logging.StreamHandler(),
                 MongoHandler(host=db_settings.HOST,
                             port=db_settings.PORT,
                             username=db_settings.USERNAME,
                             password=db_settings.PASSWORD,
                             database_name=db_settings.DATABASE_NAME,
                             collection=db_settings.LOG_COLLECTION,
                             )
                 ]

    logging.basicConfig(level=log_settings.LOG_LEVEL,
                        format=log_settings.LOG_FORMAT,
                        handlers=_handlers)
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
    log.info(f"{app_settings.APP_NAME} Application started")
    return log