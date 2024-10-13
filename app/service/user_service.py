import logging
import uuid

from app.api.vm.user_create import UserCreate
from app.api.vm.user_update import UserUpdate
from app.entity.user_entity import User
from app.repository.user_repository import UserRepository
from app.utils.pass_util import PasswordUtil

log = logging.getLogger(__name__)


class UserService:
    """
    User Business Logic Service that is responsible for handling business logic for User entity operations.

    Attributes:
    user_repository: UserRepository
        Repository for User entity operations

    """

    def __init__(self):
        log.info(f"UserService Initializing")
        self.user_repository = UserRepository()

    async def create(self, user_create: UserCreate) -> User:
        log.debug(f"UserService Creating user: {user_create} with: {type(user_create)}")

        user = User.from_create(user_create)
        user.user_id = str(uuid.uuid4())
        user.hashed_password = PasswordUtil().hash_password(user_create.password)

        result = await self.user_repository.create(user)
        log.debug(f"UserService User created: {result.user_id}")
        return result

    async def retrieve(self, user_id: str) -> User | None:
        log.debug(f"UserService Retrieving user: {user_id}")
        result = await self.user_repository.retrieve(user_id)
        log.debug(f"UserService User retrieved")
        return result

    async def list(self, query: dict, page: int, limit: int):
        log.debug(f"UserService list with query: {query}, page: {page}, limit: {limit}")
        result = await self.user_repository.list(query, page, limit)
        log.debug(f"UserService Users retrieved")
        return result

    async def update(self, user_id: str, user_update: UserUpdate | User) -> User:
        log.debug(f"UserService Updating user: {user_id} with: {type(user_update)}")
        if isinstance(user_update, UserUpdate):
            user = User.from_update(user_update)
        else:
            user = user_update
        result = await self.user_repository.update(user_id, user)
        log.debug(f"UserService User updated")
        return result

    async def delete(self, user_id: str):
        log.debug(f"UserService Deleting user: {user_id}")
        result = await self.user_repository.delete(user_id)
        log.debug(f"UserService User deleted")
        return result

    async def count(self, query: dict) -> int:
        log.debug(f"UserService Counting users with query: {query}")
        result = await self.user_repository.count(query)
        log.debug(f"UserService Users counted: {result}")
        return result

    async def retrieve_by_email(self, email: str) -> User | None:
        log.debug(f"UserService Retrieving user by email: {email}")
        result = await self.user_repository.retrieve_by_email(email)
        log.debug(f"UserService User retrieved: {result}")
        return result

    async def retrieve_by_username(self, username: str) -> User | None:
        log.debug(f"UserService Retrieving user by username: {username}")
        result = await self.user_repository.retrieve_by_username(username)
        log.debug(f"UserService User retrieved: {result}")
        return result
