import logging

from fastapi import APIRouter, HTTPException, Security, Depends
from fastapi_jwt import JwtAuthorizationCredentials

from app.config.app_settings import server_settings
from app.config.dependencies import get_user_service
from app.jwt import auth_handler
from app.security.auth_config import JWTBearer, decode_jwt_token_model
from app.security.jwt_token import JWTToken
from app.service.account_service import AccountService
from app.service.user_service import UserService

router = APIRouter(prefix=server_settings.CONTEXT_PATH, tags=["account"])

log = logging.getLogger(__name__)

jwt_security = JWTBearer()


@router.get("/me")
async def read_users_me(current_user: dict = Depends(auth_handler.get_current_user)) -> JWTToken:
    log.debug(f"AccountApi Retrieving user: {current_user}")
    jwt_token = JWTToken(**current_user)
    log.debug(f"AccountApi User retrieved")
    return jwt_token


@router.get("/account")
async def read_users_me(
        user_service: UserService = Depends(get_user_service),
        current_user: dict = Depends(auth_handler.get_current_user)):
    username = current_user["sub"]
    user = await user_service.retrieve_by_username(username)
    return user
