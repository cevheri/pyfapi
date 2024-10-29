import logging

from passlib.context import CryptContext

log = logging.getLogger(__name__)


class PasswordUtil:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_text_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_text_password, hashed_password)
