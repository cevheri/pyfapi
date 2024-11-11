from datetime import datetime

from beanie import Document
from pydantic import EmailStr


class User(Document):
    user_id: str | None = None
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    hashed_password: str | None = None
    is_active: bool | None = None
    roles: list[str] | None = None
    created_by: str | None = None
    created_date: datetime | None = None
    last_updated_by: str | None = None
    last_updated_date: datetime | None = None
    age: int | None = None

    class Settings:
        name = "app_user"
        validate_on_save = True

    def __str__(self):
        return f"User: {self.user_id}, {self.username}, {self.first_name} {self.last_name}, {self.email}, {self.is_active}, {self.roles}"
