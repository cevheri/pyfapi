import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from starlette import status

from app.api.vm.api_response import response_status_codes
from app.conf.app_settings import server_settings
from app.conf.dependencies import get_user_service
from app.schema.user_dto import UserDTO, UserCreate, UserUpdate
from app.security import auth_handler
from app.service.user_service import UserService
from app.utils.header_utils import create_list_header

_path = server_settings.CONTEXT_PATH + "/users"

router = APIRouter(prefix=_path,
                   tags=["users"],
                   dependencies=[Depends(auth_handler.get_token_user)],
                   responses=response_status_codes)
_log = logging.getLogger(__name__)


@router.post("", response_model=UserDTO, status_code=status.HTTP_201_CREATED)
async def create(user_create_data: UserCreate,
                 user_service: UserService = Depends(get_user_service),
                 token_data: dict = Depends(auth_handler.get_token_user)
                 ) -> UserDTO:
    """
    Create a new user with the provided user data.

    **user_create_data**: User data to create a new user.
    **return**: List of users

    The endpoint creates a new user with the provided user data and returns the created user's details.
    """

    _log.debug(f"UserApi Creating user: {user_create_data}  {token_data}")
    result = await user_service.create(user_create_data)
    if result is None:
        _log.error(f"UserApi User not created")
        raise HTTPException(status_code=400, detail="User not created")
    _log.debug(f"UserApi User created: {result}")
    return result


@router.get("/{user_id}", response_model=UserDTO, status_code=status.HTTP_200_OK)
async def retrieve(user_id: str,
                   user_service: UserService = Depends(get_user_service)
                   ) -> Optional[UserDTO]:
    """
    Retrieve user by user id.

    **user_id**: User id of the user to retrieve.
    **return**: User details.

    The endpoint retrieves the user by user id and returns the user details.
    """
    _log.debug(f"UserApi Retrieving user: {user_id}")
    result = await user_service.retrieve(user_id)
    if result is None:
        _log.error(f"AccountApi Account not found")
        raise HTTPException(status_code=404, detail="User not found")
    _log.debug(f"UserApi User retrieved: {result}")
    return result


@router.get("/username/{username}", response_model=UserDTO, status_code=status.HTTP_200_OK)
async def retrieve_by_username(username: str,
                               user_service: UserService = Depends(get_user_service)
                               ) -> Optional[UserDTO]:
    """
    Retrieve user by username.

    **username**: Username of the user to retrieve.
    **return**: User details.

    The endpoint retrieves the user by username and returns the user details.
    """

    _log.debug(f"UserApi Retrieving user by username: {username}")
    result = await user_service.retrieve_by_username(username)
    if result is None:
        _log.error(f"UserApi User not found")
        raise HTTPException(status_code=404, detail="User not found")
    _log.debug(f"UserApi User retrieved: {result}")
    return result


@router.get("", status_code=status.HTTP_200_OK)
async def find(query: str = None,
               page: int = 0,
               size: int = 10,
               sort: str = '+_id',
               user_service: UserService = Depends(get_user_service)
               ) -> JSONResponse:
    """
    List and filter users with the provided query, page, limit, and sort.

    **query**: Query to filter the users.
    **page**: Page number to retrieve the users.
    **limit**: Number of users to retrieve.
    **sort**: Sort the users.

    **return**: List of users

    The endpoint lists the users with the provided query, page, limit, and sort and returns the list of users.
    """
    _log.debug(f"UserApi list with query")
    page_response = await user_service.find(query, page, size, sort)
    # headers =  {"X-Total-Count": str(page_response.total)}
    headers = create_list_header(page_response)
    _log.debug(f"UserApi list retrieved with {page_response.total} records")
    json_result = [user.to_json() for user in page_response.content]
    return JSONResponse(content=json_result, headers=headers)


@router.put("/{user_id}", response_model=UserDTO, status_code=status.HTTP_200_OK)
async def update(user_id: str, user: UserUpdate,
                 user_service: UserService = Depends(get_user_service)
                 ) -> UserDTO:
    _log.debug(f"UserApi Updating user: {user_id}")
    result = await user_service.update(user_id, user)
    if result is None:
        _log.error(f"UserApi User not updated")
        raise HTTPException(status_code=400, detail="User not updated")
    _log.debug(f"UserApi User updated: {result}")
    return result


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(user_id: str,
                 user_service: UserService = Depends(get_user_service)):
    _log.debug(f"UserApi Deleting user: {user_id}")
    result = await user_service.delete(user_id)
    _log.debug(f"UserApi User deleted: {result}")
    return
