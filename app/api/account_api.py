import logging

from fastapi import APIRouter, HTTPException

from app.config.app_settings import server_settings
from app.schema.user_dto import UserDTO
from app.service.account_service import AccountService
from app.service.user_service import UserService

router = APIRouter(prefix=server_settings.CONTEXT_PATH, tags=["account"])
user_service = UserService()
account_service = AccountService()
log = logging.getLogger(__name__)

@router.get("/account", response_model=UserDTO)
async def get_account():
    log.debug(f"AccountApi Retrieving account")
    result = await account_service.get_account()
    if result is None:
        log.error(f"AccountApi Account not found")
        raise HTTPException(status_code=404, detail="Account not found")
    log.debug(f"AccountApi Account retrieved: {result}")
    return result