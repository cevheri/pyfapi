# tests/repository/test_user_repository.py
# fastapi, pydantic, beanie, mongodb unittest for user repository
import json
import logging
import uuid
from datetime import datetime, timezone

import pytest
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from testcontainers.mongodb import MongoDbContainer

from app.entity.user_entity import User
from app.repository.user_repository import UserRepository

logging.basicConfig(level=logging.ERROR)
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


# endregion init entity


# @pytest.mark.anyio
async def setup_mongo_container():
    # _log.warning("Starting mongo container")
    # global container
    container = MongoDbContainer("mongo:latest")
    container.start()
    mongo_url = container.get_connection_url()

    # global client
    client = AsyncIOMotorClient(mongo_url)

    # global db
    db = client.get_database("test")
    await db.get_collection(_collection_name).delete_many({})

    await init_beanie(database=db, document_models=[User])
    # _log.warning("Beanie initialized")
    return container


# region create entity tests
@pytest.mark.asyncio
async def test_given_min_entity_when_insert_then_successfully_created():
    _log.info("test_given_min_entity_when_insert_then_successfully_created")
    container = await setup_mongo_container()

    # Given
    entity = _get_min_entity()
    repository = _get_repo()

    # When
    result = await repository.create(entity)
    _log.info(f"{_collection_name} created: {result}")
    container.stop()
    _log.info("Container stopped")

    # Then
    assert result.user_id == entity.user_id
    assert result.username == entity.username
    assert result.first_name == entity.first_name
    assert result.last_name == entity.last_name
    assert result.email == entity.email
    assert result.hashed_password is None
    assert result.is_active == False
    assert result.roles is None
    assert result.created_by is None
    assert result.created_date is None
    assert result.last_updated_by is None
    assert result.last_updated_date is not None


@pytest.mark.asyncio
async def test_given_full_entity_when_insert_then_successfully_created():
    _log.info("test_given_full_entity_when_insert_then_successfully_created")
    container = await setup_mongo_container()

    # Given
    entity = _get_full_entity()
    repository = _get_repo()

    # When
    result = await repository.create(entity)
    _log.info(f"{_collection_name} created: {result}")

    # container.stop()
    # _log.info("Container stopped")
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
async def test_given_invalid_entity_when_insert_then_fail():
    _log.info("test_given_invalid_entity_when_insert_then_fail")
    container = await setup_mongo_container()

    # Given
    with pytest.raises(Exception):
        entity = _get_null_entity()
        repository = _get_repo()

    # When
    with pytest.raises(Exception):
        await repository.create(entity)

    container.stop()
    _log.info("Container stopped")


# endregion create entity tests

# region update entity tests
@pytest.mark.asyncio
async def test_given_entity_when_update_then_successfully_updated():
    _log.info("test_given_entity_when_update_then_successfully_updated")
    container = await setup_mongo_container()

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

    container.stop()
    _log.info("Container stopped")


@pytest.mark.asyncio
async def test_given_invalid_userid_when_update_then_fail():
    _log.info("test_given_invalid_entity_when_update_then_fail")
    container = await setup_mongo_container()

    # inti entity
    entity = _get_full_entity()
    repository = _get_repo()
    result = await repository.create(entity)

    # Given
    result.user_id = None
    # When
    with pytest.raises(Exception):
        await repository.update(result)

    container.stop()
    _log.info("Container stopped")


@pytest.mark.asyncio
async def test_given_invalid_username_when_update_then_fail():
    _log.info("test_given_invalid_entity_when_update_then_fail")
    container = await setup_mongo_container()

    # inti entity
    entity = _get_full_entity()
    repository = _get_repo()
    result = await repository.create(entity)

    # Given
    result.username = None
    # When
    with pytest.raises(Exception):
        await repository.update(result)

    container.stop()
    _log.info("Container stopped")


@pytest.mark.asyncio
async def test_given_invalid_email_when_update_then_fail():
    _log.info("test_given_invalid_entity_when_update_then_fail")
    container = await setup_mongo_container()

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

    container.stop()
    _log.info("Container stopped")


# endregion update entity tests

# region delete entity tests

@pytest.mark.asyncio
async def test_given_deleted_entity_when_retrieve_then_should_fail():
    _log.info("test_given_entity_when_delete_then_successfully_deleted")
    container = await setup_mongo_container()

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

    container.stop()
    _log.info("Container stopped")


@pytest.mark.asyncio
async def test_given_random_id_when_delete_then_should_fail():
    _log.info("test_given_entity_when_delete_then_successfully_deleted")
    container = await setup_mongo_container(),
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
async def test_given_entity_when_find_then_success():
    _log.info("test_given_entity_when_find_then_success")
    container = await setup_mongo_container()

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

    container.stop()
    _log.info("Container stopped")


# success case with mongodb query
@pytest.mark.asyncio
async def test_given_native_mogo_query_when_find_with_query_then_success():
    _log.info("test_given_entity_when_find_with_query_then_success")
    container = await setup_mongo_container()

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

    container.stop()
    _log.info("Container stopped")


# success case with query, page, size, sort
@pytest.mark.asyncio
async def test_given_native_mogo_query_when_find_with_query_page_size_sort_then_success():
    _log.info("test_given_entity_when_find_with_query_page_size_sort_then_success")
    container = await setup_mongo_container()

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

    container.stop()
    _log.info("Container stopped")


# success case with dict convert to query, page, size, sort
@pytest.mark.asyncio
async def test_given_dict_when_find_with_query_then_success():
    _log.info("test_given_entity_when_find_with_invalid_query_then_fail")
    container = await setup_mongo_container()

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

    container.stop()
    _log.info("Container stopped")


# fail case with invalid query
@pytest.mark.asyncio
async def test_given_invalid_query_when_find_with_invalid_query_then_fail():
    _log.info("test_given_entity_when_find_with_invalid_query_then_fail")
    container = await setup_mongo_container()

    # Given
    entity = _get_full_entity()
    repository = _get_repo()
    result = await repository.create(entity)
    _log.info(f"{_collection_name} created: {result}")

    # When
    with pytest.raises(Exception):
        await repository.find("invalid_query")

    # container.stop()
    _log.info("Container stopped")


# success case with count
@pytest.mark.asyncio
async def test_given_entity_when_count_then_success():
    _log.info("test_given_entity_when_count_then_success")
    container = await setup_mongo_container()

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

    container.stop()
    _log.info("Container stopped")


# fail case with count
@pytest.mark.asyncio
async def test_given_invalid_query_when_count_with_invalid_query_then_fail():
    _log.info("test_given_entity_when_count_with_invalid_query_then_fail")
    container = await setup_mongo_container()

    # Given
    entity = _get_full_entity()
    repository = _get_repo()
    result = await repository.create(entity)
    _log.info(f"{_collection_name} created: {result}")

    # When
    with pytest.raises(Exception):
        await repository.count("invalid_query")

    # container.stop()
    _log.info("Container stopped")


# success case with valid  user_id retrieve
@pytest.mark.asyncio
async def test_given_entity_when_retrieve_then_success():
    _log.info("test_given_entity_when_retrieve_then_success")
    container = await setup_mongo_container()

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

    container.stop()
    _log.info("Container stopped")


# fail case with invalid user_id retrieve
@pytest.mark.asyncio
async def test_given_invalid_user_id_when_retrieve_then_fail():
    _log.info("test_given_invalid_user_id_when_retrieve_then_fail")
    container = await setup_mongo_container()

    # Given
    entity = _get_full_entity()
    repository = _get_repo()
    result = await repository.create(entity)
    _log.info(f"{_collection_name} created: {result}")

    # When
    with pytest.raises(Exception):
        await repository.retrieve("invalid_user_id")

    container.stop()
    _log.info("Container stopped")


# success case with valid email retrieve_by_email
@pytest.mark.asyncio
async def test_given_entity_when_retrieve_by_email_then_success():
    _log.info("test_given_entity_when_retrieve_by_email_then_success")
    container = await setup_mongo_container()

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

    container.stop()
    _log.info("Container stopped")


# fail case with invalid email retrieve_by_email
@pytest.mark.asyncio
async def test_given_invalid_email_when_retrieve_by_email_then_fail():
    _log.info("test_given_invalid_email_when_retrieve_by_email_then_fail")
    container = await setup_mongo_container()

    # Given
    entity = _get_full_entity()
    repository = _get_repo()
    result = await repository.create(entity)
    _log.info(f"{_collection_name} created: {result}")

    # When
    with pytest.raises(Exception):
        await repository.retrieve_by_email("invalid_email")

    container.stop()
    _log.info("Container stopped")


# success case with valid username retrieve_by_username
@pytest.mark.asyncio
async def test_given_entity_when_retrieve_by_username_then_success():
    _log.info("test_given_entity_when_retrieve_by_username_then_success")
    container = await setup_mongo_container()

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

    container.stop()
    _log.info("Container stopped")


# fail case with invalid username retrieve_by_username
@pytest.mark.asyncio
async def test_given_invalid_username_when_retrieve_by_username_then_fail():
    _log.info("test_given_invalid_username_when_retrieve_by_username_then_fail")
    container = await setup_mongo_container()

    # Given
    entity = _get_full_entity()
    repository = _get_repo()
    result = await repository.create(entity)
    _log.info(f"{_collection_name} created: {result}")

    # When
    with pytest.raises(Exception):
        await repository.retrieve_by_username("invalid_username")

    container.stop()
    _log.info("Container stopped")

# endregion find entity tests (find with query, retrieve by id, count, retrieve by email, retrieve by username)
