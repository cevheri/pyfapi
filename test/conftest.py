# import logging
#
# import pytest
# from beanie import init_beanie
# from motor.motor_asyncio import AsyncIOMotorClient
# from testcontainers.mongodb import MongoDbContainer
#
# from app.entity.user_entity import User
#
# _log = logging.getLogger(__name__)
#
# @pytest.fixture(scope="function")
# async def mongo_container():
#     _log.info("Starting mongo container")
#     container = MongoDbContainer("mongo:latest")
#     container.start()
#     mongo_url = container.get_connection_url()
#
#     client = AsyncIOMotorClient(mongo_url)
#     db = client.get_database("testdb")
#
#     await init_beanie(database=db, document_models=[User])
#     yield db
#     container.stop()
#
# # @pytest.fixture
# # async def mock_db():
# #     client = AsyncIOMotorClient()
# #     db = client.get_database("testdb")
# #     await init_beanie(database=db, document_models=[User])
# #     yield db
# #     client.close()
