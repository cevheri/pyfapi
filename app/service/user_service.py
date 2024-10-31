import logging
import uuid
from typing import Optional

from fastapi import Depends

from app.conf.app_settings import app_settings
from app.conf.page_response import PageResponse
from app.entity.user_entity import User
from app.errors.business_exception import BusinessException, ErrorCodes
from app.repository.user_repository import UserRepository
from app.schema.user_dto import UserDTO, UserCreate, UserUpdate
from app.service.email_service import send_email
from app.utils.pass_util import PasswordUtil

log = logging.getLogger(__name__)


async def send_creation_email(user: UserDTO):
    """
    Send creation email to user with background task
    :param user: created user information
    """
    log.debug(f"UserService Sending creation email on background task to user: {user.email}")
    to = user.email
    app_name = app_settings.APP_NAME
    app_url = app_settings.APP_URL
    subject = f"Welcome to the {app_name}"
    body = f"Hello {user.first_name},\n\n" \
           f"Welcome to the {app_name}. Your account has been created successfully.\n\n" \
           f"Please visit {app_url} to login to your account.\n\n" \
           f"{app_name} Team."
    await send_email(to, subject, body)
    log.debug(f"UserService Creation email sent to user: {user.email}")


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

    async def user_create_validation(self, user_create: UserCreate):
        """
        Validate user create request
            - Check if user with email already exists
            - Check if user with username already exists
        :param user_create: UserCreate
        """
        if await User.find_one(User.username == user_create.username):
            raise BusinessException(ErrorCodes.ALREADY_EXISTS,
                                    f"User with username already exists: {user_create.username}")
        if await User.find_one(User.email == user_create.email):
            raise BusinessException(ErrorCodes.ALREADY_EXISTS,
                                    f"User with email already exists: {user_create.email}")

    async def create(self, user_create: UserCreate) -> UserDTO:
        log.debug(f"UserService Creating user: {user_create} with: {type(user_create)}")

        user = User.from_create(user_create)
        user.user_id = str(uuid.uuid4())
        user.hashed_password = PasswordUtil().hash_password(user_create.password)
        await self.user_create_validation(user_create)
        final_user = await self.user_repository.create(user)
        result = UserDTO.model_validate(final_user)
        log.debug(f"UserService User created: {result.user_id}")
        await send_creation_email(result)
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

    async def find(self, query, page: int, size: int, sort: str) -> PageResponse[UserDTO]:
        log.debug(f"UserService list request")
        entity_page_response = await self.user_repository.find(query, page, size, sort)
        page_response = PageResponse[UserDTO](
            content=[UserDTO.model_validate(user) for user in entity_page_response.content],
            page=entity_page_response.page,
            size=entity_page_response.size,
            total=entity_page_response.total,
        )

        log.debug(f"UserService Users retrieved")
        return page_response

    async def update(self, user_id: str, user_update: UserUpdate) -> Optional[UserDTO]:
        log.debug(f"UserService Updating user: {user_id} with: {type(user_update)}")

        if not user_update:
            log.debug("UserService user_update is None")
            return None

        user_entity = await self.user_repository.retrieve(user_id)
        if not user_entity:
            log.error("UserService User not found")
            return None

        for attr in ['first_name', 'last_name', 'email', 'is_active', 'roles']:
            if getattr(user_update, attr) is not None:
                setattr(user_entity, attr, getattr(user_update, attr))

        final_user = await self.user_repository.update(user_entity)
        result = UserDTO.model_validate(final_user)
        log.debug("UserService User updated")
        return result

    async def check_default_user(self, username: str):
        log.debug(f"UserService Checking default user: {username}")
        if username == "admin":
            raise BusinessException(ErrorCodes.INVALID_PAYLOAD, "Default user cannot be edited or deleted")

    async def delete(self, user_id: str) -> bool:
        log.debug(f"UserService Deleting user: {user_id}")
        await self.check_default_user(user_id)
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

    async def change_password(self, username, current_password, new_password):
        log.debug(f"UserService Validating user password: {username}")
        user = await self.user_repository.get_user_by_username(username)
        if user is None:
            raise BusinessException(ErrorCodes.NOT_FOUND, f"User not found: {username}")

        if not PasswordUtil().verify_password(current_password, user.hashed_password):
            log.error(f"AccountService Password mismatch")
            raise BusinessException(ErrorCodes.INVALID_PAYLOAD, "Password mismatch")

        user.hashed_password = PasswordUtil().hash_password(new_password)
        await self.user_repository.update(user)

        log.debug(f"UserService User password validated")
        return user
