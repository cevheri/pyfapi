from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    password: str
    is_active: bool = False
    roles: list[str]

    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@doe.com",
                "password": "plain-text-password",
                "is_active": True,
                "roles": ["admin", "user"]
            }
        }