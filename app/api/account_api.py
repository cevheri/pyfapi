import logging

from fastapi import APIRouter, Depends, Request

from app.api.vm.account_vm import ChangePasswordVM
from app.api.vm.api_response import response_status_codes
from app.conf.app_settings import server_settings
from app.conf.dependencies import get_account_service
from app.security import auth_handler
from app.security.jwt_token import JWTUser
from app.service.account_service import AccountService
from app.utils.jwt_token_utils import get_username_from_jwt_token

_path = server_settings.CONTEXT_PATH + "/account"
_log = logging.getLogger(__name__)

router = APIRouter(prefix=_path,
                   tags=["account"],
                   dependencies=[Depends(auth_handler.get_token_user)],
                   responses=response_status_codes
                   )


@router.get("")
async def get_account(
        request: Request,
        account_service: AccountService = Depends(get_account_service)):
    _log.debug(f"AccountApi read_users_me rest request")
    jwt_user = request.state.jwt_user
    user = await account_service.get_account(jwt_user.sub)
    _log.debug(f"AccountApi read_users_me rest response: {user}")
    return user


@router.get("/me", response_model=JWTUser)
async def me(request: Request) -> JWTUser:
    _log.debug(f"AccountApi Retrieving user from token")
    jwt_user = request.state.jwt_user
    _log.debug(f"AccountApi User retrieved")
    return jwt_user


@router.post("/change-password")
async def change_password(
        change_password_vm: ChangePasswordVM,
        account_service: AccountService = Depends(get_account_service),
        token_data: dict = Depends(auth_handler.get_token_user)):
    username = get_username_from_jwt_token(token_data)
    result = await account_service.change_password(username, change_password_vm)
    return result
