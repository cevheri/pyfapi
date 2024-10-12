from pydantic import BaseModel


class LoginVM(BaseModel):
    username: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "password": "plain-text-password"
            }
        }