import json
from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Body
import logging

from fastapi.openapi.models import Response

from app.api.vm.api_response import ApiResponse
from app.api.vm.user_create import UserCreate
from app.api.vm.user_update import UserUpdate
from app.config.app_settings import server_settings
from app.schema.user_dto import UserDTO
from app.service.user_service import UserService

from bson import json_util
from bson import ObjectId

# class JSONEncoder(json.JSONEncoder):
#     def default(self, o):
#         if isinstance(o, ObjectId):
#             return str(o)
#         return json.JSONEncoder.default(self, o)

router = APIRouter(prefix=server_settings.CONTEXT_PATH, tags=["users"])
user_service = UserService()
log = logging.getLogger(__name__)


@router.post("/users", response_model=ApiResponse)
async def create_user(user: UserCreate) -> ApiResponse:
    log.debug(f"UserApi Creating user: {user}")
    result = await user_service.create(user)
    log.debug(f"UserApi User created: {result.username}")
    return ApiResponse(success=True, message="User created successfully", data=result.dict())


@router.get("/users/{user_id}", response_model=ApiResponse)
async def retrieve_user(user_id: str) -> ApiResponse:
    log.debug(f"UserApi Retrieving user: {user_id}")
    result = await user_service.retrieve(user_id)
    log.debug(f"UserApi User retrieved: {result}")
    return ApiResponse(success=True, message="User retrieved successfully", data=result.dict())


@router.get("/users", response_model=list[UserDTO], response_model_exclude_unset=True)
async def list_users(query: dict=None, page: int = 0, limit: int = 10) -> ApiResponse:
    log.debug(f"UserApi list with query: {query}, page: {page}, limit: {limit}")
    entities = await user_service.list(query, page, limit)
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
