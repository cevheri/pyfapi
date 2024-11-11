import logging
from typing import Optional, Annotated

from fastapi import (
    APIRouter,
    Body,
    Depends,
    status,
    HTTPException,
    Request,
)
from fastapi.responses import JSONResponse

from app.api.vm.api_response import response_fail_status_codes
from app.conf.app_settings import server_settings
from app.conf.dependencies import get_user_service
from app.conf.query_params import QueryParams
from app.schema.user_dto import UserDTO, UserCreate, UserUpdate
from app.security import auth_handler
from app.service.user_service import UserService
from app.utils.header_utils import create_list_header

_resource = "users"
_path = f"{server_settings.CONTEXT_PATH}/{_resource}"
_log = logging.getLogger(__name__)

router = APIRouter(prefix=_path,
                   tags=[_resource],
                   dependencies=[Depends(auth_handler.get_token_user)],
                   responses=response_fail_status_codes)


@router.post(
    path="",
    operation_id="create_user",
    name="create_user",
    summary="Create user",
    response_model=UserDTO,
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_unset=True,
)
async def create(
        request: Request,
        user_create_data: Annotated[UserCreate, Body(
            ...,
            title="User Create Data",
            description="User data to create a new user.",
            alias="user_create_data",
            media_type="application/json",
            openapi_examples={
                "success_min_payload": {
                    "summary": "Min payload.",
                    "description": "Create a new user with the provided minimal user datas.",
                    "value": {
                        "username": "john_doe",
                        "email": "john@doe.com",
                        "password": "password",
                    }
                },
                "success_full_payload": {
                    "summary": "Full payload.",
                    "description": "Create a new user with the provided full user data.",
                    "value": {
                        "username": "john_doe",
                        "first_name": "John",
                        "last_name": "Doe",
                        "email": "john@doe.com",
                        "password": "password",
                        "is_active": True,
                        "roles": ["user"],
                    }
                },
                "invalid_payload": {
                    "summary": "Invalid payload",
                    "description": "Invalid payload is rejected with an error.",
                    "value": {
                        "username": "",
                        "first_name": "John",
                        "last_name": "Doe",
                        "email": "",
                    }
                }
            }
        )],
        user_service: UserService = Depends(get_user_service),
) -> UserDTO:
    """
    Create a new user with the provided user data.

    - **user_create_data**: User data to create a new user.
    - **return**: Created user details.

    The endpoint creates a new user with the provided user data and returns the created user's details.
    """
    token_data = request.state.jwt_user
    _log.debug(f"UserApi Creating user: {user_create_data}  TokenUser:{token_data}")
    result = await user_service.create(user_create_data, token_data)
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


@router.get("", response_model=list[UserDTO])
async def find(query: QueryParams = Depends(QueryParams),
               user_service: UserService = Depends(get_user_service)
               ) -> JSONResponse:
    """
    List and filter users with the provided query, page, limit, and sort.

    **query**: Query to filter the users.
    **page**: Page number to retrieve the users.
    **limit**: Number of users to retrieve.
    **sort**: Sort the users.

    **return**: List of users

    **sample usage**:
    - /users?q={"username":"john_doe1"}
    - /users?q={"age": {"$gte": 25}}
    - /users?q={"$or": [{"username": "john_doe1"}, {"age": {"$gte": 25}}]}
    - /users?q={"$and": [{"username": "john_doe1"}, {"age": {"$gte": 25}}]}
    - /users?q={"$nor": [{"username": "john_doe1"}, {"age": {"$gte": 25}}]}
    - /users?q={"username": {"$in": ["john_doe1", "john_doe2"]}}

    The endpoint lists the users with the provided query, page, limit, and sort and returns the list of users.
    """
    _log.debug(f"UserApi list with query")
    page_response = await user_service.find(query=query.q, page=query.offset, size=query.limit, sort=query.sort)
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
