from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.conf.app_settings import security_settings, server_settings
from app.security import auth_handler
from app.security.jwt_token import JWTUser

API_PREFIX = server_settings.CONTEXT_PATH
ALLOWED_PATHS = [resource for resource in security_settings.ALLOWED_PATHS]


class SecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if self._is_allowed_path(request.url.path):
            return await call_next(request)

        token = request.headers.get("Authorization")
        if not self._is_valid_token(token):
            return JSONResponse(status_code=401, content={"detail": "Unauthorized access"})

        request.state.jwt_user = self._get_user_from_token(token)
        response = await call_next(request)
        return response

    @staticmethod
    def _is_allowed_path(path: str) -> bool:
        """Check if the path is in the list of allowed paths without authorization."""
        for allowed_path in ALLOWED_PATHS:
            if allowed_path.endswith("*") and path.startswith(allowed_path[:-1]):
                return True
            if path == allowed_path:
                return True
        return False

    @staticmethod
    def _is_valid_token(token: str) -> bool:
        """Validate the authorization token."""
        return token is not None and auth_handler.is_valid_token(token.replace("Bearer ", ""))

    @staticmethod
    def _get_user_from_token(token: str) -> JWTUser:
        """Retrieve user information from the token."""
        return auth_handler.get_jwt_user_from_token(token.replace("Bearer ", ""))
