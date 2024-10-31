from pydantic import BaseModel


class LoginVM(BaseModel):
    """Login schema for authentication"""
    username: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "password": "plain-text-password"
            }
        }


class ChangePasswordVM(BaseModel):
    """Change Password schema for account"""
    current_password: str
    new_password: str

    class Config:
        json_schema_extra = {
            "example": {
                "current_password": "plain-text-current-password",
                "new_password": "plain-text-new-password"
            }
        }
