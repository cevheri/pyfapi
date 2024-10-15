from app.config.cors_config import CorsSettings
from app.config.db_config import DatabaseSettings
from app.config.email_config import SMTPSettings
from app.config.jwt_config import JWTSettings
from app.config.log_config import LoggingSettings
from app.config.server_config import ServerSettings

log_settings = LoggingSettings()
db_settings = DatabaseSettings()
cors_settings = CorsSettings()
email_settings = SMTPSettings()
server_settings = ServerSettings()
jwt_settings = JWTSettings()
