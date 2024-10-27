import logging

from fastapi import APIRouter, Depends

from app.api.vm.account_vm import ChangePasswordVM
from app.config.app_settings import server_settings
from app.config.dependencies import get_account_service
from app.security import auth_handler
from app.security.jwt_token import JWTUserToken
from app.service.account_service import AccountService
from app.utils.jwt_token_utils import get_username_from_jwt_token

router = APIRouter(prefix=server_settings.CONTEXT_PATH, tags=["account"])

log = logging.getLogger(__name__)


@router.get("/me")
async def read_users_me(token_data: dict = Depends(auth_handler.get_current_user)) -> JWTUserToken:
    log.debug(f"AccountApi Retrieving user: {token_data}")
    jwt_token = JWTUserToken(**token_data)
    log.debug(f"AccountApi User retrieved")
    return jwt_token


@router.get("/account")
async def read_users_me(
        account_service: AccountService = Depends(get_account_service),
        token_data: dict = Depends(auth_handler.get_current_user)):
    log.debug(f"AccountApi read_users_me rest request")
    username = get_username_from_jwt_token(token_data)
    user = await account_service.get_account(username)
    log.debug(f"AccountApi read_users_me rest response: {user}")
    return user


@router.post("/account/change-password")
async def change_password(
        change_password_vm: ChangePasswordVM,
        account_service: AccountService = Depends(get_account_service),
        token_data: dict = Depends(auth_handler.get_current_user)):
    username = get_username_from_jwt_token(token_data)
    result = await account_service.change_password(username, change_password_vm)
    return result
