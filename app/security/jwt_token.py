from pydantic import BaseModel, Field


class JWTUser(BaseModel):
    """
    JWT User Token Model response from the token endpoint
    """
    user_id: str = Field(alias="user_id", title="User ID")
    sub: str = Field(alias="sub", title="Username")
    email: str = Field(alias="email", title="Email")
    scopes: list[str] = Field(alias="scopes", title="Roles")
    exp: float = Field(alias="exp", title="Expires of the token")
    token: str = Field(alias="token", title="Access Token")


class JWTAccessToken(BaseModel):
    access_token: str = Field(alias="access_token", title="Access Token")
    token_type: str = Field(alias="token_type", title="Token Type (Bearer)")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.access_token = kwargs.get("access_token")
        self.token_type = kwargs.get("token_type")
