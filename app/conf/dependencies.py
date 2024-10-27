from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from app.conf.app_settings import db_settings
from app.repository.user_repository import UserRepository
from app.security.auth_service import AuthService
from app.service.account_service import AccountService
from app.service.user_service import UserService


async def get_db_client() -> AsyncIOMotorClient:
    client = AsyncIOMotorClient(db_settings.MONGODB_URI)
    try:
        yield client
    finally:
        client.close()


async def get_user_repository(db_client: AsyncIOMotorClient = Depends(get_db_client)) -> UserRepository:
    return UserRepository(db_client)


async def get_user_service(user_repository: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(user_repository)


async def get_auth_service(user_repository: UserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(user_repository)


async def get_account_service(user_service: UserService = Depends(get_user_service)) -> AccountService:
    return AccountService(user_service)
