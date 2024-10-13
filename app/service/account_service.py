import logging

from app.api.vm.account_vm import ChangePasswordVM
from app.schema.user_dto import UserDTO
from app.service.user_service import UserService
from app.utils.pass_util import PasswordUtil

log = logging.getLogger(__name__)


class AccountService:
    def __init__(self):
        log.info(f"AccountService Initializing")
        self.user_service = UserService()

    async def get_account(self) -> UserDTO | None:
        log.debug(f"AccountService Getting account")
        username = "admin"  # SecurityUtils.get_current_username()
        if username is None:
            log.error(f"AccountService User not found")
            return None
        user = await self.user_service.retrieve_by_username(username)
        if user is None:
            log.error(f"AccountService User not found")
            return None
        result = UserDTO.from_entity(user)
        log.debug(f"AccountService User found: {result}")
        return result

    async def change_password(self, change_password: ChangePasswordVM) -> bool:
        log.debug(f"AccountService Changing password")
        username = "admin"  # SecurityUtils.get_current_username()
        if username is None:
            log.error(f"AccountService User not found")
            return False
        user = await self.user_service.retrieve_by_username(username)
        if user is None:
            log.error(f"AccountService User not found")
            return False

        if not PasswordUtil().verify_password(change_password.old_password, user.password):
            log.error(f"AccountService Password mismatch")
            return False

        user.password = PasswordUtil().hash_password(password=change_password.new_password)
        result = await self.user_service.update(user.user_id, user)
        log.debug(f"AccountService Password changed for user: {result.username}")
        return True
