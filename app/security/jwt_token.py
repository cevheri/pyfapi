from pydantic import BaseModel, Field


class JWTToken(BaseModel):
    user_id: str = Field(alias="user_id")
    username: str = Field(alias="sub")
    email: str = Field(alias="email")
    roles: list[str] = Field(alias="scopes")
    expires: float = Field(alias="exp")
    token: str = Field(alias="token")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_id = kwargs.get("user_id")
        self.username = kwargs.get("sub")
        self.email = kwargs.get("email")
        self.roles = kwargs.get("scopes")
        self.expires = kwargs.get("exp")
        self.token = kwargs.get("token")

    @staticmethod
    def from_json(json_data: dict):
        return JWTToken(**json_data)
