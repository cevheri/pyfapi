from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, EmailStr, ConfigDict


# pret
class UserDTO(BaseModel):
    user_id: str = Field(..., alias="user_id", min_length=1, max_length=50, title="User ID",
                         description="Unique Identifier of the record")
    username: str = Field(..., alias="username", min_length=1, max_length=50, title="Username",
                          description="username for login")
    first_name: str = Field(..., alias="first_name", min_length=1, max_length=100, title="First Name",
                            description="First Name")
    last_name: str = Field(..., alias="last_name", min_length=1, max_length=100, title="Last Name",
                           description="Last Name")
    email: EmailStr = Field(..., alias="email", title="Email", description="Email Address")
    is_active: bool = Field(..., alias="is_active", title="Is Active", description="Record is active or not")
    roles: list[str] = Field(..., alias="roles", title="Roles", description="List of roles")
    created_by: str = Field(..., alias="created_by", min_length=1, max_length=50, title="Created By",
                            description="Created By of the record")
    created_date: datetime = Field(..., alias="created_date", title="Created Date",
                                   description="Created Date of the record")
    last_updated_by: str = Field(..., alias="last_updated_by", min_length=1, max_length=50, title="Last Updated By",
                                 description="Last Updated By of the record")
    last_updated_date: datetime = Field(..., alias="last_updated_date", title="Last Updated Date",
                                        description="Last Updated Date of the record")

    model_config = ConfigDict(
        from_attributes=True,
        title="User DTO",
        json_schema_extra={
            "example": {
                "user_id": "41ef9c67-f312-4b8f-9694-1ee1cf414c97",
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
            }})

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for k, v in kwargs.items():
            setattr(self, k, v)

    def to_json(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_active": self.is_active,
            "roles": self.roles,
            "created_by": self.created_by,
            "created_date": self.created_date.isoformat(),
            "last_updated_by": self.last_updated_by,
            "last_updated_date": self.last_updated_date.isoformat()
        }


class UserCreate(BaseModel):
    """UserCreate schema"""
    username: str = Field(..., alias="username", min_length=1, max_length=50, title="Username",
                          description="username for login")
    first_name: str = Field(..., alias="first_name", min_length=1, max_length=100, title="First Name",
                            description="First Name")
    last_name: str = Field(..., alias="last_name", min_length=1, max_length=100, title="Last Name",
                           description="Last Name")
    email: EmailStr = Field(..., alias="email", title="Email", description="Email Address")
    password: str = Field(..., alias="password", min_length=1, max_length=50, title="Password",
                          description="Plain-text password")
    is_active: bool = Field(..., alias="is_active", title="Is Active", description="Record is active or not")
    roles: list[str] = Field(..., alias="roles", title="Roles", description="List of roles")

    model_config = ConfigDict(
        from_attributes=True,
        title="User Create Model",
        json_schema_extra={
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
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for k, v in kwargs.items():
            setattr(self, k, v)


class UserUpdate(BaseModel):
    """User Update schema"""
    first_name: Optional[str] = Field(None, alias="first_name", min_length=1, max_length=100, title="First Name",
                                      description="First Name")
    last_name: Optional[str] = Field(None, alias="last_name", min_length=1, max_length=100, title="Last Name",
                                     description="Last Name")
    email: Optional[EmailStr] = Field(None, alias="email", title="Email", description="Email Address")
    is_active: Optional[bool] = Field(None, alias="is_active", title="Is Active", description="Record is active or not")
    password: str = Field(..., alias="password", min_length=1, max_length=50, title="Password",
                          description="Plain-text password")
    roles: Optional[list[str]] = Field(None, alias="roles", title="Roles", description="List of roles")

    model_config = ConfigDict(
        from_attributes=True,
        title="User Update Model",
        json_schema_extra={
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@doe.com",
                "is_active": True,
                "password": "plain-text-password",
                "roles": ["admin", "user"]
            }
        }
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for k, v in kwargs.items():
            setattr(self, k, v)
