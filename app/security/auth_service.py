from passlib.context import CryptContext

from app.repository.user_repository import UserRepository
from app.security import auth_handler


async def create_access_token_for_user(user) -> str:
    token_data = {"sub": user.username, "scopes": user.roles, "user_id": user.user_id, "email": user.email}
    return auth_handler.create_access_token(token_data)


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    async def authenticate_user(self, username: str, password: str):
        user = await self.user_repository.retrieve_by_username(username)
        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return user
