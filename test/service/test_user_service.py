# python unittest for user_service layer with mocking repository
import unittest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

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
    """
    Test suite for UserService layer. This suite mocks repository calls to test the behavior of the UserService.
    It covers various user-related operations including creation, updating, retrieval, and deletion.
    """

    async def asyncSetUp(self):
        """
        Initializes the test environment by creating a mock repository and setting up the UserService.
        It also initializes a mock MongoDB client and sets up the Beanie database.
        """
        self.mock_repository = AsyncMock()
        self.mock_email_service = AsyncMock()
        self.service = _get_service(self.mock_repository)
        self.service.email_service = self.mock_email_service
        self.client = AsyncMongoMockClient()
        await init_beanie(document_models=[User], database=self.client.get_database(name="pyfapi"))

    async def asyncTearDown(self):
        """
        Cleans up after each test by dropping the test database.
        """
        await self.client.drop_database("pyfapi")

    async def test_given_create_entity_when_create_then_send_email_success(self):
        """
        Test case: Given a valid creation entity, when a user is created,
        then an email should be sent successfully, and the user should be returned with the correct DTO.
        """
        # Arrange
        create_entity = _get_create_entity()
        jwt_user = _get_jwt_user()
        fvo = _get_mock_dto()

        self.mock_repository.create.return_value = fvo
        self.mock_email_service.send_email.return_value = True

        # Act
        result = await self.service.create(create_entity, jwt_user)

        # Assert
        self.mock_repository.create.assert_called_once()
        self.mock_email_service.send_email.assert_called_once()
        self.assertEqual(result.user_id, fvo.user_id)
        self.assertEqual(result, UserDTO.model_validate(fvo))

    async def test_given_invalid_create_entity_when_create_then_raise_invalid_payload(self):
        """
        Test case: When creating a user with an invalid entity,
        the service should raise a BusinessException with the appropriate error code.
        """
        # Arrange
        create_entity = None
        jwt_user = _get_jwt_user()

        # Act & Assert
        with self.assertRaises(BusinessException) as context:
            await self.service.create(create_entity, jwt_user)
        self.assertEqual(context.exception.code, ErrorCodes.INVALID_PAYLOAD)

    async def test_given_invalid_create_entity_when_send_email_then_raise_invalid_payload(self):
        """
        Test case: When sending an email with an invalid entity,
        the service should raise a BusinessException with the appropriate error code.
        """
        # Arrange
        dto = None
        self.mock_email_service.send_email.return_value = False

        # Act & Assert
        with self.assertRaises(BusinessException) as context:
            await self.service.send_creation_email(dto)
        self.assertEqual(context.exception.code, ErrorCodes.NOT_FOUND)

    async def test_given_invalid_email_when_create_then_fail(self):
        """
        Test case: When creating a user with an invalid email,
        the service should raise a BusinessException with the appropriate error code.
        """
        # Arrange
        create_entity = _get_create_entity()
        create_entity.email = "invalid_email@invalid.com"
        jwt_user = _get_jwt_user()

        # Act & Assert
        with self.assertRaises(Exception):
            await self.service.create(create_entity, jwt_user)


    async def test_given_existing_username_when_validation_then_raise_already_exists(self):
        """
        Test case: When creating a user with an existing email,
        it should raise a BusinessException with the appropriate error code.
        """
        # Arrange
        create_entity = _get_create_entity()
        existing_user = _get_mock_dto()
        User.find_one = AsyncMock(return_value=existing_user)

        # Act & Assert
        with self.assertRaises(BusinessException) as context:
            await self.service.user_create_validation(create_entity)
        self.assertEqual(context.exception.code, ErrorCodes.ALREADY_EXISTS)

    async def test_given_existing_email_when_validation_then_raise_already_exists(self):
        """
        Test case: When creating a user with an existing email,
        it should raise a BusinessException with the appropriate error code.
        """
        # Arrange
        create_entity = _get_create_entity()
        User.find_one = AsyncMock(side_effect=[None, _get_mock_dto()])

        # Act & Assert
        with self.assertRaises(BusinessException) as context:
            await self.service.user_create_validation(create_entity)
        self.assertEqual(context.exception.code, ErrorCodes.ALREADY_EXISTS)

    async def test_given_valid_user_id_when_retrieve_then_return_user(self):
        """
        Test case: When retrieving an existing user by user_id,
        the service should return the user DTO with the correct values.
        """
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

    async def test_given_invalid_user_id_when_retrieve_then_return_none(self):
        """
        Test case: When retrieving a user by user_id that does not exist,
        the service should return None.
        """
        # Arrange
        user_id = "test"
        self.mock_repository.retrieve.return_value = None

        # Act
        result = await self.service.retrieve(user_id)

        # Assert
        self.mock_repository.retrieve.assert_called_once_with(user_id)
        self.assertIsNone(result)

    async def test_given_valid_update_entity_when_update_then_return_user(self):
        """
        Test case: When updating an existing user,
        the service should update the user and return the correct DTO.
        """
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

    async def test_given_invalid_update_entity_when_update_then_return_none(self):
        """
        Test case: When attempting to update a user that doesn't exist,
        the service should return None.
        """
        # Arrange
        user_id = "test"
        update_entity = _get_update_entity()
        self.mock_repository.retrieve.return_value = None

        # Act
        result = await self.service.update(user_id, update_entity, _get_jwt_user())

        # Assert
        self.mock_repository.retrieve.assert_called_once_with(user_id)
        self.assertIsNone(result)

    async def test_given_null_update_entity_when_update_then_return_none(self):
        """
        Test case: When attempting to update a user with a null update entity,
        the service should return None.
        """
        # Arrange
        user_id = "test"
        update_entity = None

        # Act
        result = await self.service.update(user_id, update_entity, _get_jwt_user())

        # Assert
        self.assertIsNone(result)

    async def test_given_valid_user_when_delete_then_success(self):
        """
        Test case: When deleting an existing user by user_id,
        the service should call the delete method on the repository.
        """
        # Arrange
        user_id = "test"
        self.mock_repository.delete = AsyncMock()

        # Act
        await self.service.delete(user_id)

        # Assert
        self.mock_repository.delete.assert_called_once_with(user_id)

    async def test_given_valid_query_when_count_then_success(self):
        """
        Test case: When counting users with a given query,
        the service should return the correct count.
        """
        # Arrange
        query = {}
        self.mock_repository.count.return_value = 10

        # Act
        result = await self.service.count(query)

        # Assert
        self.mock_repository.count.assert_called_once_with(query)
        self.assertEqual(result, 10)

    async def test_given_valid_email_when_retrieve_by_email_then_success(self):
        """
        Test case: When retrieving a user by email,
        the service should return the user DTO with the correct values.
        """
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

    async def test_given_valid_username_when_retrieve_by_username_then_success(self):
        """
        Test case: When retrieving a user by username,
        the service should return the user DTO with the correct values.
        """
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

    async def test_given_valid_username_and_password_when_change_password_then_success(self):
        """
        Test case: When changing a user's password,
        the service should verify the new password and update the user's hashed password.
        """

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

    async def test_given_invalid_username_when_change_password_then_raise_not_found(self):
        """
        Test case: When changing a user's password with an invalid username,
        the service should raise a BusinessException with the appropriate error code.
        """

        # Arrange
        username = "test"
        current_password = "password"
        new_password = "new_password"
        self.mock_repository.retrieve_by_username.return_value = None

        # Act & Assert
        with self.assertRaises(BusinessException) as context:
            await self.service.change_password(username, current_password, new_password)
        self.assertEqual(context.exception.code, ErrorCodes.NOT_FOUND)

    async def test_given_not_matching_password_when_change_password_then_raise_invalid_payload(self):
        """
        Test case: When changing a user's password with a mismatched current password,
        the service should raise a BusinessException with the appropriate error code.
        """

        # Arrange
        username = "test"
        current_password = "password"
        new_password = "new_password"
        fvo = _get_mock_dto()
        self.mock_repository.retrieve_by_username.return_value = fvo

        # Act & Assert
        with self.assertRaises(BusinessException) as context:
            await self.service.change_password(username, "wrong_password", new_password)
        self.assertEqual(context.exception.code, ErrorCodes.INVALID_PAYLOAD)

    async def test_given_admin_user_when_check_default_user_then_raise_invalid_payload(self):
        """
        Test case: When checking the default user "admin",
        the service should raise a BusinessException with the appropriate error code.
        """

        # Arrange
        username = "admin"

        # Act & Assert
        with self.assertRaises(BusinessException) as context:
            await self.service.check_default_user(username)
        self.assertEqual(context.exception.code, ErrorCodes.INVALID_PAYLOAD)

    async def test_given_valid_query_when_find_then_return_users(self):
        """
        Test case: When finding users with a given query,
        the service should return the correct list of users.
        """
        # Arrange
        query = {}
        fvo = _get_mock_dto()
        page_response = MagicMock()
        page_response.content = [fvo]
        page_response.page = 0
        page_response.size = 10
        page_response.total = 1

        self.mock_repository.find.return_value = page_response

        # Act
        result = await self.service.find(query=query, page=0, size=10, sort="+_id")

        # Assert
        self.mock_repository.find.assert_called_once_with(query, 0, 10, "+_id")

        self.assertEqual(result.page, 0)
        self.assertEqual(result.size, 10)
        self.assertEqual(result.total, 1)

        self.assertEqual(result.content[0].user_id, fvo.user_id)
        self.assertEqual(result.content[0], UserDTO.model_validate(fvo))

# endregion test_service
