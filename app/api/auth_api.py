import logging

from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.vm.account_vm import LoginVM
from app.config import dependencies
from app.config.app_settings import server_settings
from app.jwt.auth_service import AuthService

router = APIRouter(prefix=server_settings.CONTEXT_PATH, tags=["auth"])

log = logging.getLogger(__name__)


# @router.post("/authenticate")
# async def authenticate(login: LoginVM = Body(...)):
#     log.debug(f"AuthAPI Authenticating user: {login.username}")
#     user = await self.user_service.retrieve_by_username(login.username)
#     if not user:
#         log.info(f"AuthAPI User not found: {login.username}")
#         return {"success": False, "message": "Incorrect email or password"}
#     if not PasswordUtil().verify_password(login.password, user.hashed_password):
#         log.info(f"AuthAPI Password not matched: {login.username}")
#         return {"success": False, "message": "Incorrect email or password"}
#
#     result = sign_jwt(user)
#     log.debug(f"AuthAPI User authenticated with token: {result}")
#     # current_user_context.set(result["access_token"])
#     return {"success": True, "message": "User authenticated successfully", "data": result}


@router.post("/login")
async def login(login_data: LoginVM,
                auth_service: AuthService = Depends(dependencies.get_auth_service)):
    log.debug(f"AuthAPI Authenticating user: {login_data.username}")
    user = await auth_service.authenticate_user(login_data.username, login_data.password)
    if not user:
        log.info(f"AuthAPI User not found: {login_data.username}")
        return {"success": False, "message": "Incorrect email or password"}
    access_token = await auth_service.create_access_token_for_user(user)
    log.debug(f"AuthAPI User authenticated with token: {access_token}")
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login/oauth")
async def login2(login_data: OAuth2PasswordRequestForm = Depends(),
                auth_service: AuthService = Depends(dependencies.get_auth_service)):
    log.debug(f"AuthAPI Authenticating user(oauth): {login_data}")
    user = await auth_service.authenticate_user(login_data.username, login_data.password)
    if not user:
        log.info(f"AuthAPI User not found: {login_data.username}")
        return {"success": False, "message": "Incorrect email or password"}
    access_token = await auth_service.create_access_token_for_user(user)
    log.debug(f"AuthAPI User authenticated with token: {access_token}")
    return {"access_token": access_token, "token_type": "bearer"}



