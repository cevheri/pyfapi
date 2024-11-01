# tests/repository/test_user_repository.py
# fastapi, pydantic, beanie, mongodb unittest for user repository
import logging
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


def get_full_entity():
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


def get_min_entity():
    user = User(
        user_id="test_user_id",
        username="test_username",
        first_name="test_first_name",
        last_name="test_last_name",
        email="test@email.com",
    )
    return user


def get_repo():
    return UserRepository()


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


@pytest.mark.asyncio
async def test_given_min_entity_when_insert_then_successfully_created():
    _log.info("test_given_min_entity_when_insert_then_successfully_created")
    container = await setup_mongo_container()

    # Given
    entity = get_min_entity()
    repo = get_repo()

    # When
    result = await repo.create(entity)
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
    entity = get_full_entity()
    repo = get_repo()

    # When
    result = await repo.create(entity)
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
        entity = User()
        repo = get_repo()

    # When
    with pytest.raises(Exception):
        await repo.create(entity)

    container.stop()
    _log.info("Container stopped")

