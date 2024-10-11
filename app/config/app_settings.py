from app.config.cors_config import CorsSettings
from app.config.db_config import DatabaseSettings
from app.config.email_config import SMTPSettings
from app.config.log_config import LoggingSettings

log_settings = LoggingSettings()
db_settings = DatabaseSettings()
cors_settings = CorsSettings()
email_settings =  SMTPSettings()