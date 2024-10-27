# Server - API configuration
from pydantic_settings import SettingsConfigDict, BaseSettings


class ServerSettings(BaseSettings):
    """
    Server configuration settings

    Attributes:
    -----------
    HOST: str
        Hostname to bind the server to
    PORT: int
        Port number to bind the server to
    DEBUG: bool
        Enable debug mode
    RELOAD: bool
        Enable auto-reload
    WORKERS: int
        Number of worker processes to spawn
    CONTEXT_PATH: str
        Base path for the API endpoints in the server like /api/v1 or /pyfapi/api/v2 etc.
    """

    model_config = SettingsConfigDict(env_prefix="SERVER_")

    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    RELOAD: bool = True
    WORKERS: int = 1
    CONTEXT_PATH: str = "/api/v1"
