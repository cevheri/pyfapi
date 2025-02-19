import logging
from typing import Annotated

from fastapi import (
    APIRouter,
    Body,
    Depends,
    Request,
    status
)

from app.api.vm.account_vm import ChangePasswordVM
from app.api.vm.api_response import response_fail_status_codes
from app.conf.app_settings import server_settings
from app.conf.dependencies import get_account_service
from app.errors.business_exception import BusinessException, ErrorCodes
from app.schema.user_dto import UserDTO
from app.security import auth_handler
from app.security.jwt_token import JWTUser
from app.service.account_service import AccountService
from app.utils.jwt_token_utils import get_username_from_jwt_token

_resource = "account"
_path = f"{server_settings.CONTEXT_PATH}/{_resource}"
_log = logging.getLogger(__name__)

router = APIRouter(prefix=_path,
                   tags=[_resource],
                   dependencies=[Depends(auth_handler.get_token_user)],
                   responses=response_fail_status_codes
                   )


@router.get(
    path="",
    operation_id="get_account",
    name="get_account",
    summary="Get account",
    response_model=UserDTO,
    status_code=status.HTTP_200_OK
)
async def get_account(
        request: Request,
        account_service: AccountService = Depends(get_account_service)) -> UserDTO | None:
    _log.debug(f"BEGIN:get_account rest request")
    jwt_user = request.state.jwt_user
    user = await account_service.get_account(jwt_user.sub)
    _log.debug(f"AccountApi read_users_me rest response: {user}")
    return user


@router.get(
    path="/me",
    operation_id="account_me",
    name="me",
    summary="Get current-user from token",
    response_model=JWTUser,
    status_code=status.HTTP_200_OK
)
async def me(request: Request) -> JWTUser:
    _log.debug(f"AccountApi Retrieving user from token")
    jwt_user = request.state.jwt_user
    _log.debug(f"AccountApi User retrieved, {jwt_user.sub}")
    return jwt_user


@router.post(
    path="/change-password",
    operation_id="change_password",
    name="change_password",
    summary="Change password for the current-user",
    response_model=bool,
)
async def change_password(
        change_password_vm: Annotated[ChangePasswordVM, Body(
            ...,
            title="Change Password",
            description="Change password request data.",
            alias="change_password_vm",
            media_type="application/json",
            openapi_examples={
                "success_min_payload": {
                    "summary": "Change password",
                    "description": "Change password for the current-user.",
                    "value": {
                        "current_password": "current_password",
                        "new_password": "new_password"
                    }
                },
                "invalid_payload": {
                    "summary": "Invalid payload",
                    "description": "Invalid payload is rejected with an error.",
                    "value": {
                        "current_password": "invalid-old-password",
                        "new_password": "new-password",
                    }
                }
            }
        )],
        account_service: AccountService = Depends(get_account_service),
        token_data: dict = Depends(auth_handler.get_token_user)) -> bool:
    _log.debug(f"AccountApi Changing password {change_password_vm}")

    if not change_password_vm.current_password or not change_password_vm.new_password:
        raise BusinessException(ErrorCodes.INVALID_PAYLOAD, "Invalid current-password or new-password")
    username = get_username_from_jwt_token(token_data)
    result = await account_service.change_password(username, change_password_vm)
    return result
