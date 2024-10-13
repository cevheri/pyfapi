# JWT token utilities
import logging
from typing import Optional

log = logging.getLogger(__name__)


class SecurityUtils:

    @staticmethod
    def get_current_username() -> Optional[str]:
        # TODO implement this method to return the current username from the request header Bearer token
        return "admin"
