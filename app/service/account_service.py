import logging

from app.api.vm.account_vm import ChangePasswordVM
from app.errors.business_exception import BusinessException, ErrorCodes
from app.schema.user_dto import UserDTO
from app.service.user_service import UserService

log = logging.getLogger(__name__)


class AccountService:
    def __init__(self, user_service: UserService):
        log.info(f"AccountService Initializing")
        self.user_service = user_service

    async def get_account(self, username: str) -> UserDTO | None:
        log.debug(f"AccountService Getting account")
        if not username:
            log.error(f"AccountService User not found")
            return None
        result = await self.user_service.retrieve_by_username(username)
        if not result:
            log.error(f"AccountService User not found")
            return None
        if not result.is_active:
            log.error(f"AccountService User is not active")
            return None
        log.debug(f"AccountService User found: {result}")
        return result

    async def change_password(self, username: str, change_password: ChangePasswordVM) -> bool:
        log.debug(f"AccountService Changing password")

        if username is None:
            log.error(f"AccountService User not found")
            raise BusinessException(ErrorCodes.NOT_FOUND, "User not found")

        if change_password.current_password == change_password.new_password:
            raise BusinessException(ErrorCodes.INVALID_PAYLOAD, "New password cannot be the same as the current password")

        await self.user_service.change_password(username, change_password.current_password, change_password.new_password)

        log.debug(f"AccountService Password changed")
        return True
