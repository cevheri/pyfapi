import logging

from fastapi import APIRouter, Body

from app.api.vm.account_vm import LoginVM
from app.config.app_settings import server_settings
from app.security.auth_config import sign_jwt
from app.service.user_service import UserService
from app.utils.pass_util import PasswordUtil

router = APIRouter(prefix=server_settings.CONTEXT_PATH, tags=["auth"])
user_service = UserService()
log = logging.getLogger(__name__)


# current_user_context: ContextVar[Optional[str]] = ContextVar("current_user_context", default=None)


@router.post("/authenticate")
async def authenticate(login: LoginVM = Body(...)):
    log.debug(f"AuthAPI Authenticating user: {login.username}")
    user = await user_service.retrieve_by_username(login.username)
    if not user:
        log.info(f"AuthAPI User not found: {login.username}")
        return {"success": False, "message": "Incorrect email or password"}
    if not PasswordUtil().verify_password(login.password, user.hashed_password):
        log.info(f"AuthAPI Password not matched: {login.username}")
        return {"success": False, "message": "Incorrect email or password"}

    result = sign_jwt(user)
    log.debug(f"AuthAPI User authenticated with token: {result}")
    # current_user_context.set(result["access_token"])
    return {"success": True, "message": "User authenticated successfully", "data": result}
