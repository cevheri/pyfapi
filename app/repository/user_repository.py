import json
import logging
from typing import Optional

from app.conf.page_response import PageResponse
from app.entity.user_entity import User
from app.errors.business_exception import BusinessException, ErrorCodes

_log = logging.getLogger(__name__)


class UserRepository:
    """
    User Repository class

    This class is responsible for handling all the database operations related to the User entity.
    User entity is a beanie document model and all the operations are performed using the beanie library.
    """

    def __init__(self):
        _log.debug(f"UserRepository Connecting to database")

    async def create(self, user: User) -> User:
        _log.debug(f"UserRepository Creating user: {user}")
        result = await User.insert(user)
        _log.debug(f"UserRepository User created")
        return result

    async def update(self, user: User) -> User | None:
        _log.debug(f"UserRepository Updating user")
        if user.user_id is None:
            raise BusinessException(ErrorCodes.INVALID_PAYLOAD, "User id is required for update")
        result = await user.replace()
        _log.debug(f"UserRepository User updated")
        return result

    async def delete(self, user_id: str):
        _log.debug(f"UserRepository Deleting user: {user_id}")
        result = await User.find_one({"user_id": user_id})
        if not result:
            raise BusinessException(ErrorCodes.NOT_FOUND, f"User not found: {user_id}")

        await result.delete()
        _log.debug(f"UserRepository User deleted")
        return

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

    async def find(self, query: str | None = None, page: int = 0, size: int = 10, sort: str = "-_id") -> PageResponse:
        _log.debug(f"UserRepository list request")
        if query is None:
            query = {}
        else:
            query = json.loads(query)

        total_count = await User.find(query).count()
        if total_count == 0:
            return PageResponse(content=[], page=page, size=size, total=total_count)

        document = User.find(query).skip(page * size).limit(size).sort(sort)
        content = await document.to_list()
        page_content = content
        _log.debug(f"UserRepository Users retrieved")
        return PageResponse(content=page_content, page=page, size=size, total=total_count)

    async def count(self, query: dict) -> int:
        _log.debug(f"UserRepository Counting users with query: {query}")
        doc = User.find(query)
        result = await doc.count()
        _log.debug(f"UserRepository Users counted")
        return result

    async def retrieve(self, user_id: str) -> User | None:
        _log.debug(f"UserRepository Retrieving user: {user_id}")
        doc = await User.find_one({"user_id": user_id})
        if not doc:
            raise BusinessException(ErrorCodes.NOT_FOUND, f"User not found: {user_id}")
        result = doc
        _log.debug(f"UserRepository User retrieved")
        return result

    async def retrieve_by_email(self, email: str) -> Optional[User]:
        _log.debug(f"UserRepository Retrieving user by email: {email}")
        doc = await User.find_one({"email": email})
        if not doc:
            raise BusinessException(ErrorCodes.NOT_FOUND, f"User not found: {email}")
        result = doc
        _log.debug(f"UserRepository User retrieved")
        return result

    async def retrieve_by_username(self, username: str) -> Optional[User]:
        _log.debug(f"UserRepository Retrieving user by username: {username}")
        doc = await User.find_one({"username": username})
        if not doc:
            raise BusinessException(ErrorCodes.NOT_FOUND, f"User not found: {username}")
        result = doc
        _log.debug(f"UserRepository User retrieved")
        return result
