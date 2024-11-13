import logging
import unittest
from datetime import datetime
from unittest.mock import patch

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.testclient import TestClient
from testcontainers.mongodb import MongoDbContainer

from app.api.user_api import get_user_service
from app.entity import User, Role
from app.main import app
from app.schema.user_dto import UserDTO
from app.security.auth_handler import get_token_user


def _get_dto():
    return UserDTO(
        first_name="test",
        last_name="test",
        email="test@test.com",
        is_active=True,
        roles=["test"],
        user_id="test",
        username="test",
        created_by="system",
        created_date=datetime(2024, 1, 1),
        last_updated_by="system",
        last_updated_date=datetime(2024, 1, 1),
    )


def mock_get_token_user():
    return {"sub": "test", "scopes": ["test"], "user_id": "test", "email": "test@test.com"}

_log = logging.getLogger(__name__)

class TestUserAPI(unittest.IsolatedAsyncioTestCase):


    def setUp(self):
        app.dependency_overrides[get_token_user] = mock_get_token_user
        self.client = TestClient(app)

    async def asyncSetUp(self):
        """
        Sets up the resources required for the tests.
        """
        _log.info("Setting up each resources.")
        self.container = MongoDbContainer(image="mongo:latest")
        self.container.start()
        self.mongo_url = self.container.get_connection_url()
        self.client = AsyncIOMotorClient(self.mongo_url)
        self.db = self.client.get_database("test")
        await init_beanie(document_models=[User, Role], database=self.db)

    def test_get_user_details(self):
        with patch('app.api.user_api.UserService') as mock_user_service:

            # Arrange
            dto = _get_dto()
            json = dto.model_dump()

            # Act
            response = self.client.get("/api/v1/users/test")

            # Assert
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), json)
