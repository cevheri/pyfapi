from typing import Optional

from pydantic import BaseModel


class UserCreate(BaseModel):
    """UserCreate schema"""
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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for k, v in kwargs.items():
            setattr(self, k, v)


class UserUpdate(BaseModel):
    """User Update schema"""
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    is_active: Optional[bool]
    roles: Optional[list[str]]

    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@doe.com",
                "is_active": True,
                "roles": ["admin", "user"]
            }
        }
