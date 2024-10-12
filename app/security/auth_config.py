from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic_settings import BaseSettings
import time
from typing import Dict

import jwt

from app.entity import User


class AuthSettings(BaseSettings):
    secret_key: str = "secret_key"
    algorithm: str = "HS256"


def token_response(token: str):
    return {"access_token": token}


def sign_jwt(user: User) -> Dict[str, str]:
    # Set the expiry time.
    payload = {"username": user.username, "roles": user.roles, "expires": time.time() + 2400}
    return token_response(jwt.encode(payload, AuthSettings().secret_key, algorithm="HS256"))


def decode_jwt(token: str) -> dict:
    decoded_token = jwt.decode(token.encode(), AuthSettings().secret_key, algorithms=["HS256"])
    return decoded_token if decoded_token["expires"] >= time.time() else {}


def verify_jwt(jwtoken: str) -> bool:
    is_token_valid: bool = False

    payload = decode_jwt(jwtoken)
    if payload:
        is_token_valid = True
    return is_token_valid


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        print("Credentials :", credentials)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication token"
                )

            if not verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token"
                )

            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization token")
