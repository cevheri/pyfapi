# JWT configuration from environment variables
from pydantic_settings import SettingsConfigDict, BaseSettings


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
    model_config = SettingsConfigDict(env_prefix="JWT_")

    ALGORITHM: str = "HS256"
    SECRET_KEY: str = "change_this_secret_key_on_env_file"
    EXPIRATION: int = 3600
