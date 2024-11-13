# import logging
# from datetime import datetime
# from unittest.mock import AsyncMock, patch
#
# import pytest
# from fastapi.testclient import TestClient
# from pydantic_settings import BaseSettings, SettingsConfigDict
#
# import app.main
# from app.conf.app_settings import server_settings
# from app.schema.user_dto import UserDTO, UserCreate
# from app.security import auth_handler
#
# _resource = "users"
# _path = f"{server_settings.CONTEXT_PATH}/{_resource}"
# _log = logging.getLogger(__name__)
#
#
# def _get_dto():
#     return UserDTO(
#         first_name="test",
#         last_name="test",
#         email="test@test.com",
#         is_active=True,
#         roles=["test"],
#         user_id="test",
#         username="test",
#         created_by="system",
#         created_date=datetime(2024, 1, 1),
#         last_updated_by="system",
#         last_updated_date=datetime(2024, 1, 1),
#     )
#
#
# def _get_fvo():
#     return UserCreate(
#         first_name="test",
#         last_name="test",
#         email="test@test.com",
#         is_active=True,
#         roles=["test"],
#         username="test",
#         password="test",
#     )
#
#
# def _get_jwt_user_dict():
#     return {"sub": "test", "scopes": ["test"], "user_id": "test", "email": "test@test.com"}
#
#
# def _get_token():
#     return auth_handler.create_access_token(_get_jwt_user_dict())
#
#
# def _get_token_user():
#     return _get_jwt_user_dict()
#
#
# def _get_header():
#     return {"Authorization": f"Bearer {_get_token()}"}
#
#
# # client = TestClient(router)
#
#
# @pytest.fixture
# def mock_user_service():
#     with patch('app.api.user_api.get_user_service', new_callable=AsyncMock) as mock:
#         yield mock
#
#
# @pytest.fixture
# def mock_auth_handler():
#     with patch('app.api.user_api.auth_handler.get_token_user', new_callable=AsyncMock) as mock:
#         yield mock
#
#
# # @pytest.fixture(scope="module")
# # def user_client():
# #     with TestClient(user_api.router) as c:
# #         yield c
#
#
#
# @pytest.fixture(scope="module")
# def client():
#     with TestClient(app=app.main.app) as c:
#         yield c
#
#
#
#
#
# @pytest.fixture(scope="module")
# def test_user():
#     return {"username": "admin", "password": "admin"}
#
#
# def test_login(client, test_user):
#     response = client.post(
#         url="/api/v1/auth/login",
#         json=test_user
#     )
#     assert response.status_code == 200
#     token = response.json()["access_token"]
#     assert token is not None
#     return token
#
#
# def test_create_user(client, mock_user_service, mock_auth_handler, test_user):
#     token = client.post(
#         url="/api/v1/auth/login",
#         data=test_user
#     )
#
#     mock_user_service.create.return_value = _get_dto()
#     fvo = _get_fvo()
#     response = client.post(
#         url=f"{_path}",
#         json=fvo.model_dump(),
#         headers=_get_header(),
#
#     )
#
#     assert response.status_code == 201
#     assert response.json()["username"] == fvo.username
#
# #
# # def test_create_user_invalid_payload(mock_user_service, mock_auth_handler):
# #     response = client.post(
# #         "/users",
# #         json={
# #             "username": "",
# #             "email": "",
# #             "password": "password"
# #         }
# #     )
# #     assert response.status_code == 422
# #
# #
# # def test_retrieve_user(mock_user_service, mock_auth_handler):
# #     mock_user_service.retrieve.return_value = UserDTO(
# #         id="1", username="john_doe", email="john@doe.com", is_active=True, roles=["user"]
# #     )
# #
# #     response = client.get("/users/1")
# #     assert response.status_code == 200
# #     assert response.json()["username"] == "john_doe"
# #
# #
# # def test_retrieve_user_not_found(mock_user_service, mock_auth_handler):
# #     mock_user_service.retrieve.return_value = None
# #
# #     response = client.get("/users/999")
# #     assert response.status_code == 404
# #
# #
# # def test_retrieve_by_username(mock_user_service, mock_auth_handler):
# #     mock_user_service.retrieve_by_username.return_value = UserDTO(
# #         id="1", username="john_doe", email="john@doe.com", is_active=True, roles=["user"]
# #     )
# #
# #     response = client.get("/users/username/john_doe")
# #     assert response.status_code == 200
# #     assert response.json()["username"] == "john_doe"
# #
# #
# # def test_retrieve_by_username_not_found(mock_user_service, mock_auth_handler):
# #     mock_user_service.retrieve_by_username.return_value = None
# #
# #     response = client.get("/users/username/unknown_user")
# #     assert response.status_code == 404
# #
# #
# # def test_find_users(mock_user_service, mock_auth_handler):
# #     mock_user_service.find.return_value = {
# #         "content": [
# #             UserDTO(id="1", username="john_doe", email="john@doe.com", is_active=True, roles=["user"])
# #         ],
# #         "total": 1
# #     }
# #
# #     response = client.get("/users?q={}")
# #     assert response.status_code == 200
# #     assert len(response.json()) == 1
# #
# #
# # def test_update_user(mock_user_service, mock_auth_handler):
# #     mock_user_service.update.return_value = UserDTO(
# #         id="1", username="john_doe_updated", email="john@doe.com", is_active=True, roles=["user"]
# #     )
# #
# #     response = client.put(
# #         "/users/1",
# #         json={
# #             "username": "john_doe_updated",
# #             "email": "john@doe.com",
# #             "is_active": True,
# #             "roles": ["user"]
# #         }
# #     )
# #     assert response.status_code == 200
# #     assert response.json()["username"] == "john_doe_updated"
# #
# #
# # def test_update_user_not_found(mock_user_service, mock_auth_handler):
# #     mock_user_service.update.return_value = None
# #
# #     response = client.put(
# #         "/users/999",
# #         json={
# #             "username": "unknown_user",
# #             "email": "unknown@user.com",
# #             "is_active": True,
# #             "roles": ["user"]
# #         }
# #     )
# #     assert response.status_code == 400
# #
# #
# # def test_delete_user(mock_user_service, mock_auth_handler):
# #     mock_user_service.delete.return_value = None
# #
# #     response = client.delete("/users/1")
# #     assert response.status_code == 204
# #
# #
# # def test_delete_user_not_found(mock_user_service, mock_auth_handler):
# #     mock_user_service.delete.return_value = None
# #
# #     response = client.delete("/users/999")
# #     assert response.status_code == 204
