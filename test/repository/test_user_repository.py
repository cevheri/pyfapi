# tests/repository/test_user_repository.py
# fastapi, pydantic, beanie, mongodb unittest for user repository
import json
import logging
import unittest
import uuid
from datetime import datetime, timezone

import pytest
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from testcontainers.mongodb import MongoDbContainer

from app.entity import Role
from app.entity.user_entity import User
from app.repository.user_repository import UserRepository

logging.basicConfig(level=logging.INFO)
logging.getLogger("pytest_asyncio").setLevel(logging.ERROR)
_log = logging.getLogger(__name__)
_collection_name = "user"


# region init entity
def _get_repo():
    return UserRepository()


def _get_full_entity():
    user = User(
        user_id="test_user_id",
        username="test_username",
        first_name="test_first_name",
        last_name="test_last_name",
        email="test@email.com",
        hashed_password="test_hashed_password",
        is_active=True,
        roles=["test_role"],
        created_by="test_created_by",
        created_date=datetime.now(timezone.utc),
        last_updated_by="test_last_updated_by",
        last_updated_date=datetime.now(timezone.utc),
    )
    return user


def _get_min_entity():
    user = User(
        user_id="test_user_id",
        username="test_username",
        first_name="test_first_name",
        last_name="test_last_name",
        email="test@email.com",
    )
    return user


def _get_null_entity():
    user = User(
        user_id=None,
        username=None,
        first_name=None,
        last_name=None,
        email=None,
        hashed_password=None,
        is_active=None,
        roles=None,
        created_by=None,
        created_date=None,
        last_updated_by=None,
        last_updated_date=None,
    )
    return user


entities = [User, Role]


# endregion init entity


class TestUserRepository(unittest.IsolatedAsyncioTestCase):
    """
      This class contains integration tests for the UserRepository, which tests the basic CRUD operations
      (Create, Read, Update, Delete) and other query functionalities. It is built using the `unittest.IsolatedAsyncioTestCase`
      to handle asynchronous setup, teardown, and test execution.

      The tests include:
      - Creating a user entity with minimal and full data and verifying the creation process.
      - Updating user entities and ensuring changes are correctly applied.
      - Handling invalid entity creation and update attempts.
      - Deleting users and verifying deletion by attempting to retrieve deleted entities.
      - Retrieving user entities with different query types (e.g., by user ID, email, or username) and ensuring correct functionality.
      - Validating error handling when invalid queries are used or when attempting to delete a non-existent user.

      The tests use a local MongoDB container (`MongoDbContainer`) for database operations during test execution. The database is
      initialized with the Beanie ODM (Object-Document Mapper) and is reset after each test to ensure clean state.

      The tests ensure that the UserRepository performs as expected in both success and failure cases, with a focus on edge
      cases and exception handling.

      Setup:
      - The MongoDB container is started in the `asyncSetUp` method, and the connection URL is used to initialize the database client.
      - Each test method runs asynchronously to simulate real-world database interactions.

      Teardown:
      - The `asyncTearDown` method ensures all data is cleared, and the MongoDB container is stopped after each test.

      These tests cover both successful cases and failure scenarios such as invalid user data or attempts to retrieve or delete
      non-existent users.
      """

    def __init__(self, *args, **kwargs):
        """
        Initializes the TestUserRepository class.
        :param args: arguments
        :param kwargs:  keyword arguments
        """
        _log.info("Initializing TestUserRepository")
        super(TestUserRepository, self).__init__(*args, **kwargs)

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
        await init_beanie(document_models=entities, database=self.db)

    async def asyncTearDown(self):
        """
        Tears down the resources after the tests.
        """
        _log.info("Tearing down each resources.")
        await self.db.get_collection(_collection_name).delete_many({})
        self.client.close()
        self.container.stop()

    # region create entity tests
    @pytest.mark.asyncio
    async def test_given_min_entity_when_insert_then_successfully_created(self):
        """
        Test case to create a user entity with minimal data and verify the creation process.
        """
        _log.info("test_given_min_entity_when_insert_then_successfully_created")
        # Given
        entity = _get_min_entity()
        repository = _get_repo()

        # When
        result = await repository.create(entity)
        _log.info(f"{_collection_name} created: {result}")

        # Then
        assert result.user_id == entity.user_id
        assert result.username == entity.username
        assert result.first_name == entity.first_name
        assert result.last_name == entity.last_name
        assert result.email == entity.email
        assert result.hashed_password is None
        assert result.is_active is None
        assert result.roles is None
        assert result.created_by is None
        assert result.created_date is None
        assert result.last_updated_by is None
        assert result.last_updated_date is None

    @pytest.mark.asyncio
    async def test_given_full_entity_when_insert_then_successfully_created(self):
        """
        Test case to create a user entity with full data and verify the creation process.
        """
        _log.info("test_given_full_entity_when_insert_then_successfully_created")

        # Given
        entity = _get_full_entity()
        repository = _get_repo()

        # When
        result = await repository.create(entity)
        _log.info(f"{_collection_name} created: {result}")

        # Then
        assert result.user_id == entity.user_id
        assert result.username == entity.username
        assert result.first_name == entity.first_name
        assert result.last_name == entity.last_name
        assert result.email == entity.email
        assert result.hashed_password == entity.hashed_password
        assert result.is_active == entity.is_active
        assert result.roles == entity.roles
        assert result.created_by == entity.created_by
        assert result.created_date is not None
        assert result.last_updated_by == entity.last_updated_by
        assert result.last_updated_date is not None

    @pytest.mark.asyncio
    async def test_given_invalid_entity_when_insert_then_fail(self):
        """
        Test case to handle invalid user entity creation attempts.
        """
        _log.info("test_given_invalid_entity_when_insert_then_fail")

        # Given
        with pytest.raises(Exception):
            entity = _get_null_entity()
            repository = _get_repo()

        # When
        with pytest.raises(Exception):
            await repository.create(entity)

    # endregion create entity tests

    # region update entity tests
    @pytest.mark.asyncio
    async def test_given_entity_when_update_then_successfully_updated(self):
        """
        Test case to update a user entity and verify the changes are correctly applied.
        """
        _log.info("test_given_entity_when_update_then_successfully_updated")

        # Given
        entity = _get_full_entity()
        repository = _get_repo()
        result = await repository.create(entity)
        _log.info(f"{_collection_name} created: {result}")

        # When
        result.first_name = "updated_first_name"
        result.last_name = "updated_last_name"
        result.email = "updated@email.com"
        result.hashed_password = "updated_hashed_password"
        result.is_active = False
        result.roles = ["updated_role"]
        result.last_updated_by = "updated_last_updated_by"
        result.last_updated_date = datetime.now(timezone.utc)

        updated_result = await repository.update(result)
        _log.info(f"{_collection_name} updated: {updated_result}")

        # Then
        assert updated_result.user_id == result.user_id
        assert updated_result.username == result.username
        assert updated_result.first_name == result.first_name
        assert updated_result.last_name == result.last_name
        assert updated_result.email == result.email
        assert updated_result.hashed_password == result.hashed_password
        assert updated_result.is_active == result.is_active
        assert updated_result.roles == result.roles
        assert updated_result.created_by == result.created_by
        assert updated_result.created_date == result.created_date
        assert updated_result.last_updated_by == result.last_updated_by
        assert updated_result.last_updated_date == result.last_updated_date

    @pytest.mark.asyncio
    async def test_given_invalid_userid_when_update_then_fail(self):
        """
        Test case to handle invalid user ID during update attempts.
        """
        _log.info("test_given_invalid_entity_when_update_then_fail")

        # inti entity
        entity = _get_full_entity()
        repository = _get_repo()
        result = await repository.create(entity)

        # Given
        result.user_id = None
        # When
        with pytest.raises(Exception):
            await repository.update(result)

    @pytest.mark.asyncio
    async def test_given_invalid_username_when_update_then_fail(self):
        """
        Test case to handle invalid username during update attempts.
        """
        _log.info("test_given_invalid_entity_when_update_then_fail")

        # inti entity
        entity = _get_full_entity()
        repository = _get_repo()
        result = await repository.create(entity)

        # Given
        result.username = None
        # When
        with pytest.raises(Exception):
            await repository.update(result)

    @pytest.mark.asyncio
    async def test_given_invalid_email_when_update_then_fail(self):
        """
        Test case to handle invalid email during update attempts.
        """
        _log.info("test_given_invalid_entity_when_update_then_fail")

        # inti entity
        entity = _get_full_entity()
        repository = _get_repo()
        result = await repository.create(entity)

        # Given
        result.email = None
        # When
        with pytest.raises(Exception):
            await repository.update(result)

        # Given
        result.email = "invalid_email"
        # When
        with pytest.raises(Exception):
            await repository.update(result)

    # endregion update entity tests

    # region delete entity tests

    @pytest.mark.asyncio
    async def test_given_deleted_entity_when_retrieve_then_should_fail(self):
        """
        Test case to handle deleted user entity retrieval attempts.
        """
        _log.info("test_given_entity_when_delete_then_successfully_deleted")

        # Given
        entity = _get_full_entity()
        repository = _get_repo()
        result = await repository.create(entity)
        _log.info(f"{_collection_name} created: {result}")

        # When
        await repository.delete(result.user_id)
        _log.info(f"{_collection_name} deleted")

        # Then
        with pytest.raises(Exception):
            await repository.retrieve(result.user_id)

    @pytest.mark.asyncio
    async def test_given_random_id_when_delete_then_should_fail(self):
        """
        Test case to handle deletion attempts for non-existent user entities.
        """
        _log.info("test_given_entity_when_delete_then_successfully_deleted")

        repository = _get_repo()

        # Given
        entity_id = str(uuid.uuid4())

        # When
        with pytest.raises(Exception):
            await repository.delete(entity_id)

    # endregion delete entity tests

    # region find entity tests (find with query, retrieve by id, count, retrieve by email, retrieve by username)

    # success case with default values
    @pytest.mark.asyncio
    async def test_given_entity_when_find_then_success(self):
        """
        Test case to find user entities and verify the results.
        """
        _log.info("test_given_entity_when_find_then_success")

        # Given
        entity = _get_full_entity()
        repository = _get_repo()
        result = await repository.create(entity)
        _log.info(f"{_collection_name} created: {result}")

        # When
        result = await repository.find()
        _log.info(f"{_collection_name} found: {result}")

        # Then
        assert result.total > 0
        assert len(result.content) > 0

    # success case with mongodb query
    @pytest.mark.asyncio
    async def test_given_native_mogo_query_when_find_with_query_then_success(self):
        """
        Test case to find user entities with a MongoDB query and verify the results.
        """
        _log.info("test_given_entity_when_find_with_query_then_success")

        # Given
        entity = _get_full_entity()
        repository = _get_repo()
        result = await repository.create(entity)
        _log.info(f"{_collection_name} created: {result}")

        # When
        result = await repository.find('{"email": "test@email.com"}')
        _log.info(f"{_collection_name} found: {result}")

        # Then
        assert result.total > 0
        assert len(result.content) > 0

    # success case with query, page, size, sort
    @pytest.mark.asyncio
    async def test_given_native_mogo_query_when_find_with_query_page_size_sort_then_success(self):
        """
        Test case to find user entities with a MongoDB query, pagination, and sorting, and verify the results.
        """
        _log.info("test_given_entity_when_find_with_query_page_size_sort_then_success")

        # Given
        entity = _get_full_entity()
        repository = _get_repo()
        result = await repository.create(entity)
        _log.info(f"{_collection_name} created: {result}")

        # When
        result = await repository.find('{"email": "test@email.com"}', 0, 10, "-_id")
        _log.info(f"{_collection_name} found: {result}")

        # Then
        assert result.total > 0
        assert len(result.content) > 0

    # success case with dict convert to query, page, size, sort
    @pytest.mark.asyncio
    async def test_given_dict_when_find_with_query_then_success(self):
        """
        Test case to find user entities with a dictionary query, pagination, and sorting, and verify the results.
        """
        _log.info("test_given_entity_when_find_with_invalid_query_then_fail")

        # Given
        entity = _get_full_entity()
        repository = _get_repo()
        result = await repository.create(entity)
        _log.info(f"{_collection_name} created: {result}")

        d = {"email": "test@email.com"}
        q = json.dumps(d)

        # When
        response = await repository.find(q, 0, 10, "-_id")
        _log.info(f"{_collection_name} found")

        assert response.total > 0
        assert len(response.content) > 0

    # fail case with invalid query
    @pytest.mark.asyncio
    async def test_given_invalid_query_when_find_with_invalid_query_then_fail(self):
        """
        Test case to handle invalid query attempts during user entity retrieval.
        """
        _log.info("test_given_entity_when_find_with_invalid_query_then_fail")

        # Given
        entity = _get_full_entity()
        repository = _get_repo()
        result = await repository.create(entity)
        _log.info(f"{_collection_name} created: {result}")

        # When
        with pytest.raises(Exception):
            await repository.find("invalid_query")

        # 

    # success case with count
    @pytest.mark.asyncio
    async def test_given_entity_when_count_then_success(self):
        """
        Test case to count user entities and verify the results.
        """
        _log.info("test_given_entity_when_count_then_success")

        # Given
        entity = _get_full_entity()
        repository = _get_repo()
        result = await repository.create(entity)
        _log.info(f"{_collection_name} created: {result}")

        # When
        result = await repository.count({})
        _log.info(f"{_collection_name} count: {result}")

        # Then
        assert result > 0

    # fail case with count
    @pytest.mark.asyncio
    async def test_given_invalid_query_when_count_with_invalid_query_then_fail(self):
        """
        Test case to handle invalid query attempts during user entity count.
        """
        _log.info("test_given_entity_when_count_with_invalid_query_then_fail")

        # Given
        entity = _get_full_entity()
        repository = _get_repo()
        result = await repository.create(entity)
        _log.info(f"{_collection_name} created: {result}")

        # When
        with pytest.raises(Exception):
            await repository.count("invalid_query")

        # 

    # success case with valid  user_id retrieve
    @pytest.mark.asyncio
    async def test_given_entity_when_retrieve_then_success(self):
        """
        Test case to retrieve a user entity by user ID and verify the results.
        """
        _log.info("test_given_entity_when_retrieve_then_success")

        # Given
        entity = _get_full_entity()
        repository = _get_repo()
        result = await repository.create(entity)
        _log.info(f"{_collection_name} created: {result}")

        # When
        result = await repository.retrieve(entity.user_id)
        _log.info(f"{_collection_name} retrieved: {result}")

        # Then
        assert result.user_id == entity.user_id
        assert result.username == entity.username
        assert result.first_name == entity.first_name
        assert result.last_name == entity.last_name
        assert result.email == entity.email

    # fail case with invalid user_id retrieve
    @pytest.mark.asyncio
    async def test_given_invalid_user_id_when_retrieve_then_fail(self):
        """
        Test case to handle invalid user ID during user entity retrieval.
        """
        _log.info("test_given_invalid_user_id_when_retrieve_then_fail")

        # Given
        entity = _get_full_entity()
        repository = _get_repo()
        result = await repository.create(entity)
        _log.info(f"{_collection_name} created: {result}")

        # When
        with pytest.raises(Exception):
            await repository.retrieve("invalid_user_id")

    # success case with valid email retrieve_by_email
    @pytest.mark.asyncio
    async def test_given_entity_when_retrieve_by_email_then_success(self):
        """
        Test case to retrieve a user entity by email and verify the results.
        """
        _log.info("test_given_entity_when_retrieve_by_email_then_success")

        # Given
        entity = _get_full_entity()
        repository = _get_repo()
        result = await repository.create(entity)
        _log.info(f"{_collection_name} created: {result}")

        # When
        result = await repository.retrieve_by_email(entity.email)
        _log.info(f"{_collection_name} retrieved: {result}")

        # Then
        assert result.user_id == entity.user_id
        assert result.username == entity.username
        assert result.first_name == entity.first_name
        assert result.last_name == entity.last_name
        assert result.email == entity.email

    # fail case with invalid email retrieve_by_email
    @pytest.mark.asyncio
    async def test_given_invalid_email_when_retrieve_by_email_then_fail(self):
        """
        Test case to handle invalid email during user entity retrieval by email.
        """
        _log.info("test_given_invalid_email_when_retrieve_by_email_then_fail")

        # Given
        entity = _get_full_entity()
        repository = _get_repo()
        result = await repository.create(entity)
        _log.info(f"{_collection_name} created: {result}")

        # When
        with pytest.raises(Exception):
            await repository.retrieve_by_email("invalid_email")

    # success case with valid username retrieve_by_username
    @pytest.mark.asyncio
    async def test_given_entity_when_retrieve_by_username_then_success(self):
        """
        Test case to retrieve a user entity by username and verify the results.
        """
        _log.info("test_given_entity_when_retrieve_by_username_then_success")

        # Given
        entity = _get_full_entity()
        repository = _get_repo()
        result = await repository.create(entity)
        _log.info(f"{_collection_name} created: {result}")

        # When
        result = await repository.retrieve_by_username(entity.username)
        _log.info(f"{_collection_name} retrieved: {result}")

        # Then
        assert result.user_id == entity.user_id
        assert result.username == entity.username
        assert result.first_name == entity.first_name
        assert result.last_name == entity.last_name
        assert result.email == entity.email

    # fail case with invalid username retrieve_by_username
    @pytest.mark.asyncio
    async def test_given_invalid_username_when_retrieve_by_username_then_fail(self):
        """
        Test case to handle invalid username during user entity retrieval by username.
        """
        _log.info("test_given_invalid_username_when_retrieve_by_username_then_fail")

        # Given
        entity = _get_full_entity()
        repository = _get_repo()
        result = await repository.create(entity)
        _log.info(f"{_collection_name} created: {result}")

        # When
        with pytest.raises(Exception):
            await repository.retrieve_by_username("invalid_username")

    # endregion find entity tests (find with query, retrieve by id, count, retrieve by email, retrieve by username)
