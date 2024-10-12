# JWT token utilities
from typing import Optional


class SecurityUtils:

    @staticmethod
    def get_current_username() -> Optional[str]:
        #TODO implement this method to return the current username from the request header Bearer token
        return "admin"