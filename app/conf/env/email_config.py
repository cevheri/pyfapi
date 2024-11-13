# Email Configuration

from pydantic_settings import BaseSettings


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

    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = "pfapi@gmail.com"
    SMTP_PASSWORD: str = "password"
    SMTP_TLS: bool = True

    class Config:
        env_prefix = "MAIL_"
        env_file = ".env.dev"
        env_file_encoding = "utf-8"
        case_sensitive = True
