from wsgiref.util import application_uri

from pydantic_settings import BaseSettings

from app.config.cors_config import CorsSettings
from app.config.db_config import DatabaseSettings
from app.config.email_config import SMTPSettings
from app.config.jwt_config import JWTSettings
from app.config.log_config import LoggingSettings
from app.config.server_config import ServerSettings

class ApplicationSettings(BaseSettings):
    """
    Application settings
    """
    APP_NAME: str = "PyFAPI"
    APP_VERSION: str = "0.1.0"
    APP_DESCRIPTION: str = "FastAPI application"
    APP_URL: str = "http://localhost:8000"
    APP_DEBUG: bool = True




app_settings = ApplicationSettings()
log_settings = LoggingSettings()
db_settings = DatabaseSettings()
cors_settings = CorsSettings()
email_settings = SMTPSettings()
server_settings = ServerSettings()
jwt_settings = JWTSettings()
