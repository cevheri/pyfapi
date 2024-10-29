from datetime import datetime, timedelta, timezone
from typing import Dict

import jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from app.conf.app_settings import jwt_settings, server_settings
from app.security.jwt_token import JWTUser

SECRET_KEY = jwt_settings.SECRET_KEY
ALGORITHM = jwt_settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = jwt_settings.EXPIRATION

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=server_settings.CONTEXT_PATH+"/auth/login/oauth")


def create_access_token(data: Dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def _decode_access_token(token: str) -> Dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        payload["token"] = token
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def is_valid_token(token: str) -> bool:
    try:
        _decode_access_token(token)
        return True
    except HTTPException:
        return False


def get_token_user(token: str = Depends(oauth2_scheme)) -> Dict:
    """
    Get the current user from the access token
    :param token: authentication token
    :return: user and token data
    """
    return _decode_access_token(token)


def get_jwt_user_from_token(token: str) -> JWTUser:
    """
    Get the current user from the access token
    :param token: authentication token
    :return: user data
    """
    jwt_user_token = JWTUser(**_decode_access_token(token))
    return jwt_user_token
