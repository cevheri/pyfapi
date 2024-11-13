# Database Configuration
import logging

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings

from app import entity

log = logging.getLogger(__name__)
client = None
db = None


class DatabaseSettings(BaseSettings):
    """
    Database settings

    Attributes:
    -----------
    MONGODB_URI: str
        MongoDB URI to connect to the database
    DATABASE_NAME: str
        Database name to connect to in MongoDB
    """

    MONGODB_URI: str | None = None
    DATABASE_NAME: str = "app"
    HOST: str = "localhost"
    PORT: int = 27017
    USERNAME: str | None = None
    PASSWORD: str | None = None
    LOG_COLLECTION: str = "app_log"

    class Config:
        env_prefix = "DB_"
        env_file = ".env.dev"
        env_file_encoding = "utf-8"
        case_sensitive = True


async def init_db():
    """
    Load database settings from the environment variables
    """
    log.info("Loading database settings")
    mongodb_uri = ""
    if DatabaseSettings().MONGODB_URI:
        mongodb_uri = DatabaseSettings().MONGODB_URI
    else:
        mongodb_uri = f"mongodb://{DatabaseSettings().HOST}:{DatabaseSettings().PORT}"
        if DatabaseSettings().USERNAME and DatabaseSettings().PASSWORD:
            mongodb_uri = f"mongodb://{DatabaseSettings().USERNAME}:{DatabaseSettings().PASSWORD}@{DatabaseSettings().HOST}:{DatabaseSettings().PORT}"

    log.debug(f"Database name: {DatabaseSettings().DATABASE_NAME}")

    global client, db
    client = AsyncIOMotorClient(mongodb_uri)
    db = client[DatabaseSettings().DATABASE_NAME]

    await init_beanie(database=db, document_models=[entity.User, entity.Role])  # TODO change-me: add more entities here
