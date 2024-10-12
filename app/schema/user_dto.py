from datetime import datetime

from pydantic import BaseModel


class UserDTO(BaseModel):
    user_id: str
    username: str
    first_name: str
    last_name: str
    email: str
    is_active: bool
    roles: list[str]
    created_by: str
    created_date: datetime
    last_updated_by: str
    last_updated_date: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "1",
                "username": "john_doe",
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@doe.com",
                "is_active": True,
                "roles": ["admin", "user"],
                "created_by": "admin",
                "created_date": "2021-01-01T00:00:00",
                "last_updated_by": "admin",
                "last_updated_date": "2021-01-01T00:00:00"
            }
        }

    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        for k, v in kwargs.items():
            setattr(self, k, v)

    @staticmethod
    def from_entity(user):
        return UserDTO(
            user_id=user.user_id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            is_active=user.is_active,
            roles=user.roles,
            created_by=user.created_by,
            created_date=user.created_date,
            last_updated_by=user.last_updated_by,
            last_updated_date=user.last_updated_date
        )
