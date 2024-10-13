import logging

from fastapi import APIRouter, HTTPException, Security
from fastapi_jwt import JwtAuthorizationCredentials

from app.config.app_settings import server_settings
from app.security.auth_config import JWTBearer, decode_jwt_token_model
from app.service.account_service import AccountService
from app.service.user_service import UserService

router = APIRouter(prefix=server_settings.CONTEXT_PATH, tags=["account"])
user_service = UserService()
account_service = AccountService()
log = logging.getLogger(__name__)

jwt_security = JWTBearer()


# TODO not implemented yet
@router.get("/account")
async def get_account():
    log.debug(f"AccountApi Retrieving account")

    result = read_current_user()
    if result is None:
        log.error(f"AccountApi Account not found")
        raise HTTPException(status_code=404, detail="Account not found")
    log.debug(f"AccountApi Account retrieved: {result}")
    return result


@router.get("/users/me")
def read_current_user(credentials: JwtAuthorizationCredentials = Security(jwt_security), ):
    return decode_jwt_token_model(credentials)
