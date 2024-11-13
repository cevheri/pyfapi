from pydantic_settings import BaseSettings


class SecuritySettings(BaseSettings):
    # TODO security.enabled not implemented yet
    ENABLED: bool = False
    # List of paths that do not require authorization like /docs,/redoc,/openapi.json,/health,/ping,/,/api/v1,/api/v1/public,/api/v1/auth/login,/api/v1/auth/register
    ALLOWED_PATHS: list[str] = []

    class Config:
        env_prefix = "SECURITY_"
        env_file = ".env.dev"
        env_file_encoding = "utf-8"
        case_sensitive = True
