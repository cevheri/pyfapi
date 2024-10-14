import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends

from app.config.app_settings import server_settings
from app.config.dependencies import get_user_service
from app.jwt.auth_handler import get_current_user
from app.schema.user_dto import UserDTO, UserCreate, UserUpdate
from app.service.user_service import UserService

router = APIRouter(prefix=server_settings.CONTEXT_PATH, tags=["users"])
log = logging.getLogger(__name__)


@router.post("/users", response_model=UserDTO)
async def create_user(user_create_data: UserCreate,
                      user_service: UserService = Depends(get_user_service),
                      current_user: dict = Depends(get_current_user)
                      ) -> UserDTO:
    """
    Create a new user with the provided user data.

    **user_create_data**: User data to create a new user.
    **return**: List of users

    The endpoint creates a new user with the provided user data and returns the created user's details.
    """

    log.debug(f"UserApi Creating user: {user_create_data}")
    result = await user_service.create(user_create_data)
    if result is None:
        log.error(f"UserApi User not created")
        raise HTTPException(status_code=400, detail="User not created")
    log.debug(f"UserApi User created: {result}")
    return result


@router.get("/users/{user_id}", response_model=UserDTO)
async def retrieve_user(self, user_id: str) -> Optional[UserDTO]:
    """
    Retrieve user by user id.

    **user_id**: User id of the user to retrieve.
    **return**: User details.

    The endpoint retrieves the user by user id and returns the user details.
    """
    log.debug(f"UserApi Retrieving user: {user_id}")
    result = await self.user_service.retrieve(user_id)
    if result is None:
        log.error(f"AccountApi Account not found")
        raise HTTPException(status_code=404, detail="User not found")
    log.debug(f"UserApi User retrieved: {result}")
    return result


@router.get("/users/username/{username}", response_model=UserDTO)
async def retrieve_user_by_username(self, username: str) -> Optional[UserDTO]:
    """
    Retrieve user by username.

    **username**: Username of the user to retrieve.
    **return**: User details.

    The endpoint retrieves the user by username and returns the user details.
    """

    log.debug(f"UserApi Retrieving user by username: {username}")
    result = await self.user_service.retrieve_by_username(username)
    if result is None:
        log.error(f"UserApi User not found")
        raise HTTPException(status_code=404, detail="User not found")
    log.debug(f"UserApi User retrieved: {result}")
    return result


@router.get("/users", response_model=list[UserDTO], response_model_exclude_unset=True)
async def list_users(self, query: str = None, page: int = 0, limit: int = 10, sort='+_id') -> Optional[list[UserDTO]]:
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
    result = await self.user_service.list(query, page, limit, sort)
    log.debug(f"UserApi list retrieved with {len(result)} records")
    return result


@router.put("/users/{user_id}", response_model=UserDTO)
async def update_user(self, user_id: str, user: UserUpdate) -> UserDTO:
    log.debug(f"UserApi Updating user: {user_id}")
    result = await self.user_service.update(user_id, user)
    if result is None:
        log.error(f"UserApi User not updated")
        raise HTTPException(status_code=400, detail="User not updated")
    log.debug(f"UserApi User updated: {result}")
    return result


@router.delete("/users/{user_id}", response_model=UserDTO)
async def delete_user(self, user_id: str) -> bool:
    log.debug(f"UserApi Deleting user: {user_id}")
    result = await self.user_service.delete(user_id)
    log.debug(f"UserApi User deleted: {result}")
    return result
