# JWT token utilities
import logging

from fastapi import FastAPI

# from app.api.auth_api import current_user_context
from app.config.app_settings import jwt_settings

log = logging.getLogger(__name__)

SECRET_KEY = jwt_settings.SECRET_KEY
ALGORITHM = jwt_settings.ALGORITHM

app = FastAPI()


# def get_current_token() -> Optional[str]:
#     return current_user_context.get()


class SecurityUtils:
    pass
    # @staticmethod
    # def get_current_token() -> Optional[str]:
    #     token = current_user_context.get(),
    #     if not verify_jwt(str(token)):
    #         return None
    #     return token
    #
    # @staticmethod
    # def get_current_username() -> Optional[str]:
    #     token = current_user_context.get()
    #     if not verify_jwt(token):
    #         return None
    #     if not token:
    #         jtw_token = SecurityUtils.get_current_user(token)
    #         return jtw_token.username
    #     return None
    #
    # @staticmethod
    # def get_current_user_dto() -> Optional[UserDTO]:
    #     token = get_current_token()
    #     if not verify_jwt(token):
    #         return None
    #
    #     if not token:
    #         jwt_token = SecurityUtils.get_current_user(token)
    #     else:
    #         return None
    #
    #     user = User.find_one({"username": jwt_token.username})
    #     user_dto = UserDTO.from_entity(user)
    #     return user_dto
