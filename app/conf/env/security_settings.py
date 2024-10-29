from pydantic_settings import BaseSettings, SettingsConfigDict


class SecuritySettings(BaseSettings):
    prefix: str = "SECURITY_"
    model_config = SettingsConfigDict(env_prefix=prefix)

    # TODO security.enabled not implemented yet
    ENABLED: bool = False
    # List of paths that do not require authorization like /docs,/redoc,/openapi.json,/health,/ping,/,/api/v1,/api/v1/public,/api/v1/auth/login,/api/v1/auth/register
    ALLOWED_PATHS: list[str] = []
