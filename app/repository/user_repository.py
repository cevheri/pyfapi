import json
import logging
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient

from app.conf.app_settings import db_settings
from app.conf.page_response import PageResponse
from app.entity.user_entity import User

log = logging.getLogger(__name__)


class UserRepository:

    def __init__(self, db_client: AsyncIOMotorClient):
        self.db_client = db_client
        self.db = db_client[db_settings.DATABASE_NAME]
        self.collection = self.db.get_collection(User.get_collection_name())

    async def create(self, user: User) -> User:
        log.debug(f"UserRepository Creating user: {user}")
        doc = await self.collection.insert_one(user.model_dump())
        log.debug(f"UserRepository User created _id: {doc.inserted_id}")
        return user

    async def retrieve(self, user_id: str) -> User | None:
        log.debug(f"UserRepository Retrieving user: {user_id}")
        doc = await self.collection.find_one({"user_id": user_id})
        if not doc:
            return None
        result = User(**doc)
        log.debug(f"UserRepository User retrieved")
        return result

    # TODO - Implement the find method
    #        # Parse the query string if provided, otherwise set to an empty dict
    #         try:
    #             mongo_query = json.loads(query) if query else {}
    #         except json.JSONDecodeError as e:
    #             raise HTTPException(status_code=400, detail="Invalid query format") from e
    #
    #         # MongoDB count_documents for total count
    #         total_count = await self.collection.count_documents(mongo_query)
    #         if total_count == 0:
    #             return PageResponse(content=[], page=page, size=size, total=total_count)
    #
    #         # Build the MongoDB cursor with optional sorting, pagination, and limit
    #         cursor = self.collection.find(mongo_query)
    #         if sort:
    #             sort_field, sort_order = (sort.split(":") + ["asc"])[:2]
    #             sort_order = 1 if sort_order.lower() == "asc" else -1
    #             cursor = cursor.sort(sort_field, sort_order)
    #
    #         cursor = cursor.skip(page * size).limit(size)
    #
    #         # Retrieve results and map to User model
    #         content = await cursor.to_list(length=size)
    #         page_content = [User(**doc) for doc in content]

    async def find(self, query: str, page: int, size: int, sort: str) -> PageResponse[User]:
        log.debug(f"UserRepository list request")
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

    async def update(self, user: User) -> User | None:
        log.debug(f"UserRepository Updating user")
        result = await self.collection.update_one({"user_id": user.user_id}, {"$set": user.model_dump()})
        log.debug(f"UserRepository User updated: {result}")
        return user

    async def delete(self, user_id: str) -> bool:
        log.debug(f"UserRepository Deleting user: {user_id}")
        result = await self.collection.delete_one({"user_id": user_id})
        log.debug(f"UserRepository User deleted: {result.deleted_count}")
        return result.deleted_count > 0

    async def count(self, query: dict) -> int:
        log.debug(f"UserRepository Counting users with query: {query}")
        result = await self.collection.count_documents(query)
        log.debug(f"UserRepository Users counted: {result}")
        return result

    async def get_user_by_email(self, email: str) -> Optional[User]:
        log.debug(f"UserRepository Retrieving user by email: {email}")
        doc = await self.collection.find_one({"email": email})
        result = User(**doc)
        log.debug(f"UserRepository User retrieved")
        return result

    async def get_user_by_username(self, username: str) -> Optional[User]:
        log.debug(f"UserRepository Retrieving user by username: {username}")
        doc = await self.collection.find_one({"username": username})
        result = User(**doc)
        log.debug(f"UserRepository User retrieved")
        return result
