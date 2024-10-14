import logging

from fastapi import HTTPException, Depends

from app.jwt import auth_handler

log = logging.getLogger(__name__)


def get_curren_user(token: str = Depends(auth_handler.oauth2_scheme)) -> dict:
    log.debug(f"AuthHandler Getting current user")
    payload = auth_handler.decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload
