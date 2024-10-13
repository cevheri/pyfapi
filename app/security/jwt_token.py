from pydantic import BaseModel


class JWTToken(BaseModel):
    username: str
    roles: list[str]
    expires: float
    token: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.username = kwargs.get("username")
        self.roles = kwargs.get("roles")
        self.expires = kwargs.get("expires")
        self.token = kwargs.get("token")

    @staticmethod
    def from_json(json_data: dict):
        return JWTToken(**json_data)