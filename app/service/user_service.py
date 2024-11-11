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
from app.security.jwt_token import JWTUser
from app.service import email_service
from app.utils.pass_util import PasswordUtil

_log = logging.getLogger(__name__)


class UserService:
    """
    User Business Logic Service that is responsible for handling business logic for User entity operations.

    Attributes:
    user_repository: UserRepository
        Repository for User entity operations

    """

    def __init__(self, user_repository: UserRepository = Depends()):
        _log.info("UserService Initializing")
        self.repository = user_repository
        self.email_service = email_service

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

    async def send_creation_email(self, user: UserDTO):
        """
        Send creation email to user with background task
        :param user: created user information
        """
        _log.debug(f"Sending creation email on background task")
        if user is None:
            raise BusinessException(ErrorCodes.NOT_FOUND, "User not found")

        to = user.email
        app_name = app_settings.APP_NAME
        app_url = app_settings.APP_URL
        subject = f"Welcome to the {app_name}"
        body = f"Hello {user.first_name},\n\n" \
               f"Welcome to the {app_name}. Your account has been created successfully.\n\n" \
               f"Please visit {app_url} to login to your account.\n\n" \
               f"{app_name} Team."
        await self.email_service.send_email(to, subject, body)
        _log.debug(f"Sent Creation email sent to user: {user.email}")

    async def create(self, user_create: UserCreate, token_data: JWTUser) -> UserDTO:
        _log.debug(f"UserService Creating user: {user_create} with: {type(user_create)}")

        try:
            hashed_password = PasswordUtil().hash_password(user_create.password)
            user = User(**user_create.model_dump(), hashed_password=hashed_password)
            user.created_by = token_data.sub
            user.last_updated_by = token_data.sub
            user.user_id = str(uuid.uuid4())

            await self.user_create_validation(user_create)
            final_user = await self.repository.create(user)
            result = UserDTO.model_validate(final_user)
        except Exception as e:
            raise BusinessException(
                ErrorCodes.INVALID_PAYLOAD, f"Error creating user: {e}"
            ) from e

        _log.debug(f"UserService User created: {result.user_id}")
        try:
            await self.send_creation_email(result)
        except Exception as e:
            _log.error(f"UserService Error sending creation email: {e}")
        return result

    async def retrieve(self, user_id: str) -> Optional[UserDTO]:
        _log.debug(f"UserService Retrieving user: {user_id}")
        final_user = await self.repository.retrieve(user_id)
        if final_user is None:
            _log.error("UserService User not found")
            return None
        result = UserDTO.model_validate(final_user)
        _log.debug("UserService User retrieved")
        return result

    async def find(self, query, page: int, size: int, sort: str) -> PageResponse[UserDTO]:
        _log.debug("UserService list request")
        entity_page_response = await self.repository.find(query, page, size, sort)
        page_response = PageResponse[UserDTO](
            content=[UserDTO.model_validate(user) for user in entity_page_response.content],
            page=entity_page_response.page,
            size=entity_page_response.size,
            total=entity_page_response.total,
        )

        _log.debug("UserService Users retrieved")
        return page_response

    async def update(self, user_id: str, user_update: UserUpdate, token_data: JWTUser) -> Optional[UserDTO]:
        _log.debug(f"UserService Updating user: {user_id} with: {type(user_update)}")

        if not user_update:
            _log.debug("UserService user_update is None")
            return None

        user_entity = await self.repository.retrieve(user_id)
        if not user_entity:
            _log.error("UserService User not found")
            return None

        for attr in ['first_name', 'last_name', 'email', 'is_active', 'roles']:
            if getattr(user_update, attr) is not None:
                setattr(user_entity, attr, getattr(user_update, attr))

        user_entity.last_updated_by = token_data.sub
        final_user = await self.repository.update(user_entity)
        result = UserDTO.model_validate(final_user)
        _log.debug("UserService User updated")
        return result

    async def check_default_user(self, username: str):
        _log.debug(f"UserService Checking default user: {username}")
        if username == "admin":
            raise BusinessException(ErrorCodes.INVALID_PAYLOAD, "Default user cannot be edited or deleted")

    async def delete(self, user_id: str):
        _log.debug(f"Deleting user: {user_id}")
        await self.check_default_user(user_id)
        await self.repository.delete(user_id)
        _log.debug("Deleted user")

    async def count(self, query: dict) -> int:
        _log.debug(f"UserService Counting users with query: {query}")
        result = await self.repository.count(query)
        _log.debug(f"UserService Users counted: {result}")
        return result

    async def retrieve_by_email(self, email: str) -> Optional[UserDTO]:
        _log.debug(f"UserService Retrieving user by email: {email}")
        final_user = await self.repository.retrieve_by_email(email)
        result = UserDTO.model_validate(final_user)
        _log.debug(f"UserService User retrieved: {result}")
        return result

    async def retrieve_by_username(self, username: str) -> Optional[UserDTO]:
        _log.debug(f"UserService Retrieving user by username: {username}")
        final_user = await self.repository.retrieve_by_username(username)
        result = UserDTO.model_validate(final_user)
        _log.debug(f"UserService User retrieved: {result}")
        return result

    async def change_password(self, username: str, current_password: str, new_password: str):
        _log.debug(f"Validating user password: {username}")
        user = await self.repository.retrieve_by_username(username)
        if user is None:
            raise BusinessException(ErrorCodes.NOT_FOUND, f"User not found: {username}")

        if not PasswordUtil().verify_password(current_password, user.hashed_password):
            _log.error("AccountService Password mismatch")
            raise BusinessException(ErrorCodes.INVALID_PAYLOAD, "Password mismatch")

        user.hashed_password = PasswordUtil().hash_password(new_password)
        await self.repository.update(user)

        _log.debug("Validated user password")
