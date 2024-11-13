import logging
import unittest
from unittest.mock import patch

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.testclient import TestClient
from testcontainers.mongodb import MongoDbContainer

from app.main import app
from app.entity import db_entities
from app.security.auth_handler import get_token_user

_log = logging.getLogger(__name__)


def mock_get_token_user():
    return {"sub": "test", "scopes": ["test"], "user_id": "test", "email": "test@test.com"}

app.dependency_overrides[get_token_user] = mock_get_token_user
client = TestClient(app=app)


class TestAuthAPI(unittest.IsolatedAsyncioTestCase):


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
        await init_beanie(document_models=db_entities, database=self.db)

    async def asyncTearDown(self):
        """
        Tears down the resources after the tests.
        """
        _log.info("Tearing down each resources.")
        self.client.close()
        self.container.stop()

    def test_authentication_endpoint(self):
        with patch('app.security.auth_service.AuthService.authenticate_user') as mock_authenticate_user:
            mock_authenticate_user.return_value = True
            response = client.post("api/v1/auth/login", json={"username": "testuser", "password": "testpass"})
            assert response.status_code == 200
            assert "access_token" in response.json()

            response = client.post("api/v1/auth/login", json={"username": "testuser", "password": "testpass"})
            assert response.status_code == 200
            assert "access_token" in response.json()

    def test_invalid_authentication(self):
        response = client.post("api/v1/auth/login", json={"username": "wronguser", "password": "wrongpass"})
        assert response.status_code == 401
        assert "detail" in response.json()
