import logging
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.vm.account_vm import LoginVM
from app.api.vm.api_response import response_fail_status_codes
from app.conf import dependencies
from app.conf.app_settings import server_settings
from app.security.auth_service import create_access_token_for_user, AuthService
from app.security.jwt_token import JWTAccessToken

_resource = "auth"
_path = f"{server_settings.CONTEXT_PATH}/{_resource}"
_log = logging.getLogger(__name__)
router = APIRouter(
    prefix=_path,
    tags=[_resource],
    responses=response_fail_status_codes)


@router.post(
    path="/login",
    operation_id="jwt_login",
    name="jwt_login",
    summary="Login with username and password",
    response_model=JWTAccessToken,
    status_code=status.HTTP_200_OK,
)
async def jwt_login(
        login_data: Annotated[LoginVM, Body(
            ...,
            title="Login Data",
            description="Login data with username and password.",
            alias="login_data",
            openapi_examples={
                "min_payload": {
                    "summary": "Min payload.",
                    "description": "Login with the provided minimal login data.",
                    "value": {
                        "username": "admin",
                        "password": "admin",
                    }
                },
                "full_payload": {
                    "summary": "Full payload.",
                    "description": "Login with the provided full login data.",
                    "value": {
                        "username": "admin",
                        "password": "admin",
                        "remember": True
                    }
                },
                "invalid_payload": {
                    "summary": "Invalid payload.",
                    "description": "Login with the provided invalid username or password.",
                    "value": {
                        "username": "invalid_username",
                        "password": "invalid_password"
                    }
                }
            }
        )],
        auth_service: AuthService = Depends(dependencies.get_auth_service)) -> JWTAccessToken:
    """
    Login with username and password to get the access token.

    **login_data**: Login data with username and password.

    **return**: JWT Access token.

    The endpoint authenticates the user with the provided username and password and returns the access token.
    """
    _log.debug(f"AuthAPI username and password authenticating")
    user = await auth_service.authenticate_user(login_data.username, login_data.password)
    if not user:
        _log.info(f"AuthAPI User not found: {login_data.username}")
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token = await create_access_token_for_user(user)
    result = JWTAccessToken(access_token=access_token, token_type="bearer")
    _log.debug(f"AuthAPI User authenticated with token: {result}")
    return result


@router.post(
    path="/login/oauth",
    operation_id="oauth_login",
    name="oauth_login",
    summary="OAuth login",
    response_model=JWTAccessToken,
    status_code=status.HTTP_200_OK,
)
async def oauth_login(oauth_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
                      auth_service: AuthService = Depends(
                          dependencies.get_auth_service)) -> HTTPException | JWTAccessToken:
    """
    Login with OAuth to get the access token.

    **oauth_data**: OAuth data with username and password (Optional : **grant_type**, **scope**, **client_id**, **client_secret**).

    **return**: JWT Access token

    The endpoint authenticates the user with the provided OAuth data and returns the access token.
    """

    _log.debug(f"AuthAPI oauth authenticating user: {oauth_data}")
    user = await auth_service.authenticate_user(oauth_data.username, oauth_data.password)
    if not user:
        _log.info(f"AuthAPI User not found: {oauth_data.username}")
        return HTTPException(status_code=401, detail="Incorrect email or password")
    access_token = await create_access_token_for_user(user)
    result = JWTAccessToken(access_token=access_token, token_type="bearer")
    _log.debug(f"AuthAPI oauth authenticated with token: {result}")
    return result
