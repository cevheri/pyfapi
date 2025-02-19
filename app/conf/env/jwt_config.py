# JWT configuration from environment variables
from pydantic_settings import BaseSettings


class JWTSettings(BaseSettings):
    """
    JWT configuration settings

    Attributes:
    -----------
    JWT_ALGORITHM: str
        Algorithm to use for encoding and decoding JWT tokens
    JWT_SECRET_KEY: str
        Secret key to use for encoding and decoding JWT tokens
    JWT_EXPIRATION: int
        Expiration time for JWT tokens in seconds
    """

    ALGORITHM: str = "HS256"
    EXPIRATION: int = 86400
    SECRET_KEY: str = "change_this_secret_key_on_env_file"

    class Config:
        env_prefix = "JWT_"
        env_file = ".env.dev"
        env_file_encoding = "utf-8"
        case_sensitive = True
