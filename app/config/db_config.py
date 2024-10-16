# Database Configuration
import logging

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings, SettingsConfigDict

from app import entity

log = logging.getLogger(__name__)
client = None
db = None


# , cli_parse_args=True for dev or prod environments like uvicorn run app:app --host "" --port 8080 --profile dev
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

    model_config = SettingsConfigDict(env_prefix="DB_")

    MONGODB_URI: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "app"


async def init_db():
    """
    Load database settings from the environment variables
    """
    log.info("Loading database settings")
    # log.debug(f"Database URI: {DatabaseSettings().MONGODB_URI}")
    log.debug(f"Database name: {DatabaseSettings().DATABASE_NAME}")

    global client, db
    client = AsyncIOMotorClient(DatabaseSettings().MONGODB_URI)
    db = client[DatabaseSettings().DATABASE_NAME]

    await init_beanie(database=db, document_models=[entity.User, entity.Role])
