import json
import logging
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient

from app.config.app_settings import db_settings
from app.config.page_response import PageResponse
from app.entity.user_entity import User

log = logging.getLogger(__name__)


class UserRepository:

    def __init__(self, db_client: AsyncIOMotorClient):
        self.db_client = db_client
        self.db = db_client[db_settings.DATABASE_NAME]
        self.collection = self.db.get_collection(User.get_collection_name())

    async def create(self, user: User) -> User:
        log.debug(f"UserRepository Creating user: {user}")
        result = await self.collection.insert_one(user.model_dump())
        log.debug(f"UserRepository User created _id: {result.inserted_id}")
        return user

    async def retrieve(self, user_id: str) -> User | None:
        log.debug(f"UserRepository Retrieving user: {user_id}")
        result = await self.collection.find_one({"user_id": user_id})
        if not result:
            return None
        user = User.model_load(result)
        log.debug(f"UserRepository User retrieved")
        return user

    async def find(self, query: str, page: int, size: int, sort: str) -> PageResponse[User]:
        log.debug(f"UserRepository list request")
        # TODO  set defaults if not provided. defaults are page=0, limit=10, sort=["+_id"] and should be set in environment or config or constants
        if query is None:
            query = {}
        else:
            query = json.loads(query)

        total_count = await self.collection.count_documents(query)
        if total_count == 0:
            return PageResponse(content=[], page=page, size=size, total=total_count)

        document = self.collection.find(query).skip(page * size).limit(size).sort(sort)
        content = await document.to_list()
        page_content = [User(**doc) for doc in content]
        log.debug(f"UserRepository Users retrieved")
        return PageResponse(content=page_content, page=page, size=size, total=total_count)

    async def update(self, user_id: str, user: User) -> User | None:
        log.debug(f"UserRepository Updating user: {user_id}")
        # update with merge patch
        org_user = await User.find_one(User.user_id == user_id)
        if not org_user:
            return None
        updated_user = user.model_dump(exclude_unset=True)
        result = await org_user.update(updated_user)
        log.debug(f"UserRepository User updated: {result.username}")
        return result

    async def delete(self, user_id: str) -> bool:
        log.debug(f"UserRepository Deleting user: {user_id}")
        result = await User.delete_one(User.user_id == user_id)
        log.debug(f"UserRepository User deleted: {result.username}")
        return result

    async def count(self, query: dict) -> int:
        log.debug(f"UserRepository Counting users with query: {query}")
        result = await User.count_documents(query)
        log.debug(f"UserRepository Users counted: {result.username}")
        return result

    async def get_user_by_email(self, email: str) -> Optional[User]:
        log.debug(f"UserRepository Retrieving user by email: {email}")
        result = await User.find_one(User.email == email)
        log.debug(f"UserRepository User retrieved")
        return result

    async def get_user_by_username(self, username: str) -> Optional[User]:
        log.debug(f"UserRepository Retrieving user by username: {username}")
        result = await User.find_one(User.username == username)
        log.debug(f"UserRepository User retrieved")
        return result
