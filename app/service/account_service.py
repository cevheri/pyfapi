import logging

from app.api.vm.change_password_vm import ChangePasswordVM
from app.entity.user_entity import User
from app.security.security_utils import SecurityUtils
from app.utils.pass_util import PasswordUtil

log = logging.getLogger(__name__)


class AccountService:
    def __init__(self, user_service):
        log.info(f"AccountService Initializing")
        self.user_service = user_service

    def get_account(self) -> User | None:
        log.debug(f"AccountService Getting account")
        username = SecurityUtils.get_current_username()
        if username is None:
            log.error(f"AccountService User not found")
            return None
        user = self.user_service.retrieve_by_username(username)
        if user is None:
            log.error(f"AccountService User not found")
            return None
        log.debug(f"AccountService User found: {user}")
        return user

    def change_password(self, change_password: ChangePasswordVM) -> bool:
        log.debug(f"AccountService Changing password")
        username = SecurityUtils.get_current_username()
        if username is None:
            log.error(f"AccountService User not found")
            return False
        user = self.user_service.retrieve_by_username(username)
        if user is None:
            log.error(f"AccountService User not found")
            return False

        if not PasswordUtil().verify_password(change_password.old_password, user.password):
            log.error(f"AccountService Password mismatch")
            return False

        user.password = PasswordUtil().hash_password(password=change_password.new_password)
        result = self.user_service.update(user.user_id, user)
        log.debug(f"AccountService Password changed for user: {result.username}")
        return True
