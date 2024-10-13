import logging

from fastapi import APIRouter, HTTPException

from app.api.vm.api_response import ApiResponse
from app.api.vm.user_vm import UserCreate, UserUpdate
from app.config.app_settings import server_settings
from app.schema.user_dto import UserDTO
from app.service.user_service import UserService

router = APIRouter(prefix=server_settings.CONTEXT_PATH, tags=["users"])
user_service = UserService()
log = logging.getLogger(__name__)


@router.post("/users", response_model=ApiResponse)
async def create_user(user_create_data: UserCreate) -> ApiResponse:
    """
    Create a new user with the provided user data.

    **user_create_data**: User data to create a new user.
    **return**: List of users

    The endpoint creates a new user with the provided user data and returns the created user's details.
    """

    log.debug(f"UserApi Creating user: {user_create_data}")
    result = await user_service.create(user_create_data)
    log.debug(f"UserApi User created: {result.username}")
    return ApiResponse(success=True, message="User created successfully", data=result.dict())


@router.get("/users/{user_id}", response_model=ApiResponse)
async def retrieve_user(user_id: str) -> ApiResponse:
    log.debug(f"UserApi Retrieving user: {user_id}")
    result = await user_service.retrieve(user_id)
    if result is None:
        log.error(f"AccountApi Account not found")
        raise HTTPException(status_code=404, detail="Account not found")
    log.debug(f"UserApi User retrieved: {result}")
    return ApiResponse(success=True, message="User retrieved successfully", data=result.dict())


@router.get("/users", response_model=list[UserDTO], response_model_exclude_unset=True)
async def list_users(query: str=None, page: int=0, limit: int=10, sort='+_id') -> list[UserDTO]:
    """
    List and filter users with the provided query, page, limit, and sort.

    **query**: Query to filter the users.
    **page**: Page number to retrieve the users.
    **limit**: Number of users to retrieve.
    **sort**: Sort the users.

    **return**: List of users

    The endpoint lists the users with the provided query, page, limit, and sort and returns the list of users.
    """

    log.debug(f"UserApi list with query: {query}, page: {page}, limit: {limit}, sort: {sort}")
    entities = await user_service.list(query, page, limit, sort)
    result = UserDTO.from_entities(entities)
    log.debug(f"UserApi list retrieved with {len(result)} records")
    return result


@router.put("/users/{user_id}", response_model=ApiResponse)
async def update_user(user_id: str, user: UserUpdate) -> ApiResponse:
    log.debug(f"UserApi Updating user: {user_id}")
    result = await user_service.update(user_id, user)
    log.debug(f"UserApi User updated: {result}")
    return ApiResponse(success=True, message="User updated successfully", data=result.dict())


@router.delete("/users/{user_id}", response_model=ApiResponse)
async def delete_user(user_id: str) -> ApiResponse:
    log.debug(f"UserApi Deleting user: {user_id}")
    result = await user_service.delete(user_id)
    log.debug(f"UserApi User deleted: {result}")
    return ApiResponse(success=True, message="User deleted successfully", data=result)
