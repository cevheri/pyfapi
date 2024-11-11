# python unittest for user_service layer with mocking repository
import unittest
from datetime import datetime
from unittest.mock import AsyncMock, patch, MagicMock

from beanie import init_beanie
from mongomock_motor import AsyncMongoMockClient

from app.entity import User
from app.errors.business_exception import BusinessException, ErrorCodes
from app.schema.user_dto import UserCreate, UserUpdate
from app.schema.user_dto import UserDTO
from app.security.jwt_token import JWTUser
from app.service.user_service import UserService
from app.utils.pass_util import PasswordUtil


# region init entity

def _get_jwt_user():
    return JWTUser(
        user_id="system",
        sub="system",
        email="system@system.com",
        scopes=["system"],
        exp=1000,
        token="token",
    )


def _get_create_entity():
    return UserCreate(
        first_name="test",
        last_name="test",
        email="test@test.com",
        is_active=True,
        roles=["test"],
        username="test",
        password="password",
    )


def _get_update_entity():
    return UserUpdate(
        first_name="test",
        last_name="test",
        email="test@test.com",
        is_active=True,
        roles=["test"],
    )


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


def _get_mock_dto():
    dto = MagicMock()
    dto.first_name = "test"
    dto.last_name = "test"
    dto.email = "test@test.com"
    dto.is_active = True
    dto.roles = ["test"]
    dto.user_id = "test"
    dto.username = "test"
    dto.created_by = "system"
    dto.created_date = datetime(2024, 1, 1)
    dto.last_updated_by = "system"
    dto.last_updated_date = datetime(2024, 1, 1)
    dto.password = "password"
    dto.hashed_password = PasswordUtil().hash_password("password")
    return dto


def _get_service(repository):
    return UserService(user_repository=repository)


# endregion init entity


# region test_service
class TestUserService(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.mock_repository = AsyncMock()
        self.service = _get_service(self.mock_repository)
        self.client = AsyncMongoMockClient()
        await init_beanie(document_models=[User], database=self.client.get_database(name="pyfapi"))

    async def asyncTearDown(self):
        await self.client.drop_database("pyfapi")

    @patch("app.service.user_service.send_creation_email", new_callable=AsyncMock)
    async def test_given_create_entity_when_create_then_send_email_success(self, mock_send_email):
        # Arrange
        create_entity = _get_create_entity()
        jwt_user = _get_jwt_user()

        fvo = _get_mock_dto()

        self.mock_repository.create.return_value = fvo

        # Act
        result = await self.service.create(create_entity, jwt_user)

        # Assert
        self.mock_repository.create.assert_called_once()
        mock_send_email.assert_called_once_with(UserDTO.model_validate(fvo))
        self.assertEqual(result.user_id, fvo.user_id)
        self.assertEqual(result, UserDTO.model_validate(fvo))

    async def test_user_create_validation_user_exists(self):
        # Arrange
        create_entity = _get_create_entity()
        existing_user = _get_mock_dto()
        User.find_one = AsyncMock(return_value=existing_user)

        # Act & Assert
        with self.assertRaises(BusinessException) as context:
            await self.service.user_create_validation(create_entity)
        self.assertEqual(context.exception.code, ErrorCodes.ALREADY_EXISTS)

    async def test_retrieve_user_success(self):
        # Arrange
        user_id = "test"
        fvo = _get_mock_dto()
        self.mock_repository.retrieve.return_value = fvo

        # Act
        result = await self.service.retrieve(user_id)

        # Assert
        self.mock_repository.retrieve.assert_called_once_with(user_id)
        self.assertEqual(result.user_id, fvo.user_id)
        self.assertEqual(result, UserDTO.model_validate(fvo))

    async def test_retrieve_user_not_found(self):
        # Arrange
        user_id = "test"
        self.mock_repository.retrieve.return_value = None

        # Act
        result = await self.service.retrieve(user_id)

        # Assert
        self.mock_repository.retrieve.assert_called_once_with(user_id)
        self.assertIsNone(result)

    async def test_update_user_success(self):
        # Arrange
        user_id = "test"
        update_entity = _get_update_entity()
        fvo = _get_mock_dto()
        self.mock_repository.retrieve.return_value = fvo
        self.mock_repository.update.return_value = fvo

        # Act
        result = await self.service.update(user_id, update_entity, _get_jwt_user())

        # Assert
        self.mock_repository.retrieve.assert_called_once_with(user_id)
        self.mock_repository.update.assert_called_once()
        self.assertEqual(result.user_id, fvo.user_id)
        self.assertEqual(result, UserDTO.model_validate(fvo))

    async def test_update_user_not_found(self):
        # Arrange
        user_id = "test"
        update_entity = _get_update_entity()
        self.mock_repository.retrieve.return_value = None

        # Act
        result = await self.service.update(user_id, update_entity, _get_jwt_user())

        # Assert
        self.mock_repository.retrieve.assert_called_once_with(user_id)
        self.assertIsNone(result)

    async def test_delete_user_success(self):
        # Arrange
        user_id = "test"
        self.mock_repository.delete = AsyncMock()

        # Act
        await self.service.delete(user_id)

        # Assert
        self.mock_repository.delete.assert_called_once_with(user_id)

    async def test_count_users(self):
        # Arrange
        query = {}
        self.mock_repository.count.return_value = 10

        # Act
        result = await self.service.count(query)

        # Assert
        self.mock_repository.count.assert_called_once_with(query)
        self.assertEqual(result, 10)

    async def test_retrieve_by_email_success(self):
        # Arrange
        email = "test@test.com"
        fvo = _get_mock_dto()
        self.mock_repository.retrieve_by_email.return_value = fvo

        # Act
        result = await self.service.retrieve_by_email(email)

        # Assert
        self.mock_repository.retrieve_by_email.assert_called_once_with(email)
        self.assertEqual(result.user_id, fvo.user_id)
        self.assertEqual(result, UserDTO.model_validate(fvo))

    async def test_retrieve_by_username_success(self):
        # Arrange
        username = "test"
        fvo = _get_mock_dto()
        self.mock_repository.retrieve_by_username.return_value = fvo

        # Act
        result = await self.service.retrieve_by_username(username)

        # Assert
        self.mock_repository.retrieve_by_username.assert_called_once_with(username)
        self.assertEqual(result.user_id, fvo.user_id)
        self.assertEqual(result, UserDTO.model_validate(fvo))

    async def test_change_password_success(self):
        # Arrange
        username = "test"
        current_password = "password"
        new_password = "new_password"
        fvo = _get_mock_dto()
        self.mock_repository.retrieve_by_username.return_value = fvo

        # Act
        await self.service.change_password(username, current_password, new_password)

        # Assert
        self.mock_repository.retrieve_by_username.assert_called_once_with(username)
        self.mock_repository.update.assert_called_once()
        self.assertTrue(PasswordUtil().verify_password(new_password, fvo.hashed_password))
# endregion test_service
