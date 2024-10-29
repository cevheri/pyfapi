# Cors configuration from Environment Variables
from pydantic_settings import BaseSettings, SettingsConfigDict


class CorsSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CORS_")

    ALLOWED_ORIGINS: str = "*"
    ALLOWED_METHODS: str = "GET, POST, PUT, DELETE, OPTIONS"
    ALLOWED_HEADERS: str = "*"
    ALLOW_CREDENTIALS: bool = True
    MAX_AGE: int = 3600
