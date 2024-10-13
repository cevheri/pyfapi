import logging

from app.api.vm.user_vm import UserCreate
from app.entity import Role
from app.service.user_service import UserService

log = logging.getLogger(__name__)
user_service = UserService()


async def init_default_user():
    log.info(f"Initializing default user")
    res = await user_service.retrieve_by_username("admin")
    if res:
        log.info(f"Default user already exists")
        return
    user_create = UserCreate(
        username="admin",
        first_name="Admin",
        last_name="User",
        email="admin@localhost.com",
        password="admin",
        is_active=True,
        roles=["admin"]
    )
    await user_service.create(user_create)
    log.info(f"Default user initialized")


async def init_roles():
    log.info(f"Initializing roles")
    res = await Role.find_one(Role.name == "admin")
    if not res:
        await Role(name="admin").create()
    res = await Role.find_one(Role.name == "user")
    if not res:
        await Role(name="user").create()
    log.info(f"Default roles initialized")


async def init_migration():
    log.info(f"Initializing migration")
    await init_roles()
    await init_default_user()
    log.info(f"Migration initialized")
