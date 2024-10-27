from datetime import datetime, timedelta, timezone
from typing import Dict

import jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from app.config.app_settings import jwt_settings

SECRET_KEY = jwt_settings.SECRET_KEY
ALGORITHM = jwt_settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = jwt_settings.EXPIRATION

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/oauth")


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


def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict:
    """
    Get the current user from the access token
    :param token: authentication token
    :return: user and token data
    """
    return _decode_access_token(token)
