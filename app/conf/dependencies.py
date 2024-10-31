from fastapi import Depends

from app.repository.user_repository import UserRepository
from app.security.auth_service import AuthService
from app.service.account_service import AccountService
from app.service.user_service import UserService


async def get_user_repository() -> UserRepository:
    return UserRepository()


async def get_user_service(user_repository: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(user_repository)


async def get_auth_service(user_repository: UserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(user_repository)


async def get_account_service(user_service: UserService = Depends(get_user_service)) -> AccountService:
    return AccountService(user_service)
