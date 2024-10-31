import json
import logging
from typing import Optional

from app.conf.page_response import PageResponse
from app.entity.user_entity import User
from app.errors.business_exception import BusinessException, ErrorCodes

_log = logging.getLogger(__name__)


class UserRepository:

    def __init__(self):
        _log.debug(f"UserRepository Connecting to database")

    async def create(self, user: User) -> User:
        _log.debug(f"UserRepository Creating user: {user}")
        doc = await User.insert(user)
        _log.debug(f"UserRepository User created _id: {doc}")
        return user

    async def retrieve(self, user_id: str) -> User | None:
        _log.debug(f"UserRepository Retrieving user: {user_id}")
        doc = await User.find_one({"user_id": user_id})
        if not doc:
            raise BusinessException(ErrorCodes.NOT_FOUND, f"User not found: {user_id}")
        result = doc
        _log.debug(f"UserRepository User retrieved")
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

    async def find(self, query: str, page: int, size: int, sort: str) -> PageResponse:
        _log.debug(f"UserRepository list request")
        if query is None:
            query = {}
        else:
            query = json.loads(query)

        doc = User.find(query)
        total_count = await doc.count()
        if total_count == 0:
            return PageResponse(content=[], page=page, size=size, total=total_count)

        document = User.find(query).skip(page * size).limit(size).sort(sort)
        content = await document.to_list()
        page_content = content
        _log.debug(f"UserRepository Users retrieved")
        return PageResponse(content=page_content, page=page, size=size, total=total_count)


    async def update(self, user: User) -> User | None:
        _log.debug(f"UserRepository Updating user")
        result = await user.replace()
        _log.debug(f"UserRepository User updated: {result}")
        return user

    @staticmethod
    async def delete(user_id: str) -> bool:
        _log.debug(f"UserRepository Deleting user: {user_id}")
        result = await User.find_one({"user_id": user_id}).delete()
        _log.debug(f"UserRepository User deleted: {result.deleted_count}")
        return result.deleted_count > 0

    @staticmethod
    async def count(query: dict) -> int:
        _log.debug(f"UserRepository Counting users with query: {query}")
        doc = User.find(query)
        result = await doc.count()
        _log.debug(f"UserRepository Users counted: {result}")
        return result

    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        _log.debug(f"UserRepository Retrieving user by email: {email}")
        doc = await User.find_one({"email": email})
        result = doc
        _log.debug(f"UserRepository User retrieved")
        return result

    @staticmethod
    async def get_user_by_username(username: str) -> Optional[User]:
        _log.debug(f"UserRepository Retrieving user by username: {username}")
        doc = await User.find_one({"username": username})
        result = doc
        _log.debug(f"UserRepository User retrieved")
        return result
