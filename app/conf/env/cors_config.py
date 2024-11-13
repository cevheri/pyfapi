# Cors configuration from Environment Variables
from pydantic_settings import BaseSettings


class CorsSettings(BaseSettings):
    ALLOWED_ORIGINS: str = "*"
    ALLOWED_METHODS: str = "GET, POST, PUT, DELETE, OPTIONS"
    ALLOWED_HEADERS: str = "*"
    ALLOW_CREDENTIALS: bool = True
    MAX_AGE: int = 3600

    class Config:
        env_prefix = "CORS_"
        env_file = ".env.dev"
        env_file_encoding = "utf-8"
        case_sensitive = True
