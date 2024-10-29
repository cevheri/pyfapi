from pydantic_settings import BaseSettings

from app.conf.cors_config import CorsSettings
from app.conf.db_config import DatabaseSettings
from app.conf.email_config import SMTPSettings
from app.conf.jwt_config import JWTSettings
from app.conf.log_config import LoggingSettings
from app.conf.security_settings import SecuritySettings
from app.conf.server_config import ServerSettings


class ApplicationSettings(BaseSettings):
    """
    Application settings
    """
    APP_NAME: str = "PyFAPI"
    APP_VERSION: str = "0.1.0"
    APP_DESCRIPTION: str = "Python FastAPI mongodb app for Enterprise usage with best practices, tools, and more."
    APP_URL: str = "http://localhost:8000"
    APP_DEBUG: bool = True


app_settings = ApplicationSettings()
log_settings = LoggingSettings()
db_settings = DatabaseSettings()
cors_settings = CorsSettings()
email_settings = SMTPSettings()
server_settings = ServerSettings()
jwt_settings = JWTSettings()
security_settings = SecuritySettings()
