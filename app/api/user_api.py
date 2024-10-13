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


@router.post("/users", response_model=UserDTO)
async def create_user(user_create_data: UserCreate) -> ApiResponse:
    """
    Create a new user with the provided user data.

    **user_create_data**: User data to create a new user.
    **return**: List of users

    The endpoint creates a new user with the provided user data and returns the created user's details.
    """

    log.debug(f"UserApi Creating user: {user_create_data}")
    user = await user_service.create(user_create_data)
    if user is None:
        log.error(f"UserApi User not created")
        raise HTTPException(status_code=400, detail="User not created")
    result = UserDTO.from_entity(user)
    log.debug(f"UserApi User created: {result}")
    return result


@router.get("/users/{user_id}", response_model=UserDTO)
async def retrieve_user(user_id: str):
    """
    Retrieve user by user id.

    **user_id**: User id of the user to retrieve.
    **return**: User details.

    The endpoint retrieves the user by user id and returns the user details.
    """
    log.debug(f"UserApi Retrieving user: {user_id}")
    user = await user_service.retrieve(user_id)
    if user is None:
        log.error(f"AccountApi Account not found")
        raise HTTPException(status_code=404, detail="User not found")
    result = UserDTO.from_entity(user)
    log.debug(f"UserApi User retrieved: {result}")
    return result


@router.get("/users/username/{username}", response_model=UserDTO)
async def retrieve_user_by_username(username: str):
    """
    Retrieve user by username.

    **username**: Username of the user to retrieve.
    **return**: User details.

    The endpoint retrieves the user by username and returns the user details.
    """

    log.debug(f"UserApi Retrieving user by username: {username}")
    user = await user_service.retrieve_by_username(username)
    if user is None:
        log.error(f"UserApi User not found")
        raise HTTPException(status_code=404, detail="User not found")
    result = UserDTO.from_entity(user)
    log.debug(f"UserApi User retrieved: {result}")
    return result


@router.get("/users", response_model=list[UserDTO], response_model_exclude_unset=True)
async def list_users(query: str = None, page: int = 0, limit: int = 10, sort='+_id') -> list[UserDTO]:
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


@router.put("/users/{user_id}", response_model=UserDTO)
async def update_user(user_id: str, user: UserUpdate):
    log.debug(f"UserApi Updating user: {user_id}")
    user = await user_service.update(user_id, user)
    if user is None:
        log.error(f"UserApi User not updated")
        raise HTTPException(status_code=400, detail="User not updated")
    result = UserDTO.from_entity(user)
    log.debug(f"UserApi User updated: {result}")
    return result


@router.delete("/users/{user_id}", response_model=UserDTO)
async def delete_user(user_id: str):
    log.debug(f"UserApi Deleting user: {user_id}")
    result = await user_service.delete(user_id)
    log.debug(f"UserApi User deleted: {result}")
    return result
