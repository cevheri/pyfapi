import logging
import uuid
from typing import Optional

from fastapi import Depends

from app.entity.user_entity import User
from app.repository.user_repository import UserRepository
from app.schema.user_dto import UserDTO, UserCreate, UserUpdate
from app.utils.pass_util import PasswordUtil

log = logging.getLogger(__name__)


class UserService:
    """
    User Business Logic Service that is responsible for handling business logic for User entity operations.

    Attributes:
    user_repository: UserRepository
        Repository for User entity operations

    """

    def __init__(self, user_repository: UserRepository = Depends()):
        log.info(f"UserService Initializing")
        self.user_repository = user_repository

    async def create(self, user_create: UserCreate) -> UserDTO:
        log.debug(f"UserService Creating user: {user_create} with: {type(user_create)}")

        user = User.from_create(user_create)
        user.user_id = str(uuid.uuid4())
        user.hashed_password = PasswordUtil().hash_password(user_create.password)

        final_user = await self.user_repository.create(user)
        result = UserDTO.model_validate(final_user)
        log.debug(f"UserService User created: {result.user_id}")
        return result

    async def retrieve(self, user_id: str) -> Optional[UserDTO]:
        log.debug(f"UserService Retrieving user: {user_id}")
        final_user = await self.user_repository.retrieve(user_id)
        if final_user is None:
            log.error(f"UserService User not found")
            return None
        result = UserDTO.model_validate(final_user)
        log.debug(f"UserService User retrieved")
        return result

    async def list(self, query, page, limit, sort) -> Optional[list[UserDTO]]:
        log.debug(f"UserService list with query: {query}, page: {page}, limit: {limit}, sort: {sort}")
        final_users = await self.user_repository.list(query, page, limit, sort)
        if final_users is None:
            log.error(f"UserService Users not found")
            return None
        result = [UserDTO.model_validate(user) for user in final_users]
        log.debug(f"UserService Users retrieved")
        return result

    async def update(self, user_id: str, user_update: UserUpdate | User) -> UserDTO:
        log.debug(f"UserService Updating user: {user_id} with: {type(user_update)}")
        if isinstance(user_update, UserUpdate):
            user = User.from_update(user_update)
        else:
            user = user_update
        final_user = await self.user_repository.update(user_id, user)
        result = UserDTO.model_validate(final_user)
        log.debug(f"UserService User updated")
        return result

    async def delete(self, user_id: str) -> bool:
        log.debug(f"UserService Deleting user: {user_id}")
        result = await self.user_repository.delete(user_id)
        log.debug(f"UserService User deleted")
        return result

    async def count(self, query: dict) -> int:
        log.debug(f"UserService Counting users with query: {query}")
        result = await self.user_repository.count(query)
        log.debug(f"UserService Users counted: {result}")
        return result

    async def retrieve_by_email(self, email: str) -> Optional[UserDTO]:
        log.debug(f"UserService Retrieving user by email: {email}")
        final_user = await self.user_repository.get_user_by_email(email)
        result = UserDTO.model_validate(final_user)
        log.debug(f"UserService User retrieved: {result}")
        return result

    async def retrieve_by_username(self, username: str) -> Optional[UserDTO]:
        log.debug(f"UserService Retrieving user by username: {username}")
        final_user = await self.user_repository.get_user_by_username(username)
        result = UserDTO.model_validate(final_user)
        log.debug(f"UserService User retrieved: {result}")
        return result
