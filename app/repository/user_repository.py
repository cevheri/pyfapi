import logging
from typing import List

from app.entity.user_entity import User

log = logging.getLogger(__name__)


class UserRepository:
    async def create(self, user: User) -> User:
        log.debug(f"UserRepository Creating user: {user}")
        result = await user.create()
        log.debug(f"UserRepository User created: {result.user_id}")
        return result

    async def retrieve(self, user_id: str) -> User | None:
        log.debug(f"UserRepository Retrieving user: {user_id}")
        result = await User.find_one(User.user_id == user_id)
        log.debug(f"UserRepository User retrieved: {result.username}")
        return result

    async def list(self, query: dict = None, page: int = 0, limit: int = 10, sort=None) -> List[User]:
        if sort is None:
            sort = {"_id": 1}
        log.debug(f"UserRepository list with query: {query}, page: {page}, limit: {limit}, sort: {sort}")
        result = await User.find(query, skip=page, limit=limit).to_list()
        log.debug(f"UserRepository Users retrieved")
        return result

    # mongodb update when user field is not null if user field is null, it will not update
    async def update(self, user_id: str, user: User) -> User | None:
        log.debug(f"UserRepository Updating user: {user_id}")
        # update with merge patch
        org_user = await User.find_one(User.user_id == user_id)
        if not org_user:
            return None
        updated_user = user.dict(exclude_unset=True)
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

    async def retrieve_by_email(self, email: str) -> User | None:
        log.debug(f"UserRepository Retrieving user by email: {email}")
        result = await User.find_one(User.email == email)
        log.debug(f"UserRepository User retrieved: {result.username}")
        return result

    async def retrieve_by_username(self, username: str) -> User | None:
        log.debug(f"UserRepository Retrieving user by username: {username}")
        result = await User.find_one(User.username == username)
        log.debug(f"UserRepository User retrieved: {result.username}")
        return result
