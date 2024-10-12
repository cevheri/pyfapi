from datetime import datetime

from pydantic import BaseModel, validator, field_validator


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

    # def to_dict(self)-> dict:
    #     return {
    #         "user_id": self.user_id,
    #         "username": self.username,
    #         "first_name": self.first_name,
    #         "last_name": self.last_name,
    #         "email": self.email,
    #         "is_active": self.is_active,
    #         "roles": self.roles,
    #         "created_by": self.created_by,
    #         "created_date": self.created_date.isoformat(),
    #         "last_updated_by": self.last_updated_by,
    #         "last_updated_date": self.last_updated_date.isoformat()
    #     }

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

    @staticmethod
    def from_entities(users):
        return [UserDTO.from_entity(user) for user in users]

    # @classmethod
    # @field_validator("created_date")
    # def validate_created_date(self, value):
    #     if not value:
    #         return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
    #     return value
    #
    # @classmethod
    # @field_validator("last_updated_date")
    # def validate_last_updated_date(cls, value):
    #     if not value:
    #         return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
    #     return value