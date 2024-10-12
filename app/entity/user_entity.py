import uuid
from datetime import datetime, timezone
from typing import Optional

from beanie import Document
from beanie import PydanticObjectId
from bson import ObjectId

from app.api.vm.user_create import UserCreate
from app.api.vm.user_update import UserUpdate
from app.schema.user_dto import UserDTO



class User(Document):
    user_id: Optional[str] = None
    username: str
    first_name: str
    last_name: str
    email: str
    hashed_password: Optional[str] = None
    is_active: bool = False
    roles: list[str]
    created_by: Optional[str] = None
    created_date: Optional[datetime] = None
    last_updated_by: str
    last_updated_date: datetime = datetime.now(timezone.utc)

    class Settings:
        collection = "app_user"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for k, v in kwargs.items():
            setattr(self, k, v)

    @staticmethod
    def from_create(user_create: UserCreate):
        return User(
            user_id="",
            username=user_create.username,
            first_name=user_create.first_name,
            last_name=user_create.last_name,
            email=user_create.email,
            hashed_password="",
            is_active=user_create.is_active,
            roles=user_create.roles,
            created_by="system",
            created_date=datetime.now().isoformat(),
            last_updated_by="system",
            last_updated_date=datetime.now().isoformat(),
        )

    @staticmethod
    def from_update(user_update: UserUpdate):
        return User(
            user_id="",  # Not allowed to update
            username="",  # Not allowed to update
            first_name=user_update.first_name,
            last_name=user_update.last_name,
            email=user_update.email,
            hashed_password="",  # Not allowed to update
            is_active=user_update.is_active,
            roles=user_update.roles,
            created_by="",  # Not allowed to update
            created_date=None,  # Not allowed to update
            last_updated_by="system",
            last_updated_date=datetime.now(timezone.utc)
        )

    @staticmethod
    def from_dto(user_dto: UserDTO):
        return User(
            user_id=user_dto.user_id,
            first_name=user_dto.first_name,
            last_name=user_dto.last_name,
            email=user_dto.email,
            is_active=user_dto.is_active,
            roles=user_dto.roles,
            created_by=user_dto.created_by,
            created_date=user_dto.created_date,
            last_updated_by=user_dto.last_updated_by,
            last_updated_date=user_dto.last_updated_date
        )

    def __str__(self):
        return f"User: {self.user_id}, {self.first_name} {self.last_name}, {self.email}, {self.is_active}, {self.roles}"
