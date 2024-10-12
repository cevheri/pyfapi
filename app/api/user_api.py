from fastapi import APIRouter
import logging as log

from app.api.vm.api_response import ApiResponse
from app.api.vm.user_create import UserCreate
from app.api.vm.user_update import UserUpdate
from app.config.app_settings import server_settings
from app.service.user_service import UserService

router = APIRouter(prefix=server_settings.CONTEXT_PATH, tags=["users"])
user_service = UserService()


@router.post("/users", response_model=ApiResponse)
async def create_user(user: UserCreate) -> ApiResponse:
    log.debug(f"UserAPI Creating user: {user}")
    result = await user_service.create(user)
    log.debug(f"UserAPI User created: {result.username}")
    return ApiResponse(success=True, message="User created successfully", data=result.dict())


@router.get("/users/{user_id}", response_model=ApiResponse)
async def retrieve_user(user_id: str) -> ApiResponse:
    log.debug(f"UserAPI Retrieving user: {user_id}")
    result = await user_service.retrieve(user_id)
    log.debug(f"UserAPI User retrieved: {result}")
    return ApiResponse(success=True, message="User retrieved successfully", data=result.dict())


@router.get("/users", response_model=ApiResponse)
async def list_users(query: dict = None, page: int = 0, limit: int = 10) -> ApiResponse:
    log.debug(f"UserAPI Listing users with query: {query}, page: {page}, limit: {limit}")
    result = await user_service.list(query, page, limit)
    log.debug(f"UserAPI Users retrieved: {len(result)}")
    return ApiResponse(success=True, message="Users retrieved successfully", data=[user.dict() for user in result])


@router.put("/users/{user_id}", response_model=ApiResponse)
async def update_user(user_id: str, user: UserUpdate) -> ApiResponse:
    log.debug(f"UserAPI Updating user: {user_id}")
    result = await user_service.update(user_id, user)
    log.debug(f"UserAPI User updated: {result}")
    return ApiResponse(success=True, message="User updated successfully", data=result.dict())


@router.delete("/users/{user_id}", response_model=ApiResponse)
async def delete_user(user_id: str) -> ApiResponse:
    log.debug(f"UserAPI Deleting user: {user_id}")
    result = await user_service.delete(user_id)
    log.debug(f"UserAPI User deleted: {result}")
    return ApiResponse(success=True, message="User deleted successfully", data=result)
