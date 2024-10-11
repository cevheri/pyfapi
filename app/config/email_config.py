# Email Configuration

from pydantic_settings import BaseSettings, SettingsConfigDict


class SMTPSettings(BaseSettings):
    """
    SMTP settings

    Attributes:
    -----------
    SMTP_HOST: str
        SMTP server hostname
    SMTP_PORT: int
        SMTP server port
    SMTP_USERNAME: str
        SMTP server username
    SMTP_PASSWORD: str
        SMTP server password
    SMTP_TLS: bool
        SMTP server TLS
    """

    model_config = SettingsConfigDict(env_prefix="MAIL_")

    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = "pfapi@gmail.com"
    SMTP_PASSWORD: str = "password"
    SMTP_TLS: bool = True
