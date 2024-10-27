import logging
import uuid
from datetime import datetime, timezone

from app.entity import Role, User
from app.utils.pass_util import PasswordUtil

log = logging.getLogger(__name__)


async def init_roles():
    log.info(f"Initializing roles")
    res = await Role.find_one(Role.name == "admin")
    if not res:
        await Role(name="admin").create()
    res = await Role.find_one(Role.name == "user")
    if not res:
        await Role(name="user").create()
    log.info(f"Default roles initialized")


async def init_default_user():
    log.info(f"Initializing default user")
    res = await User.find_one(User.username == "admin")
    if res:
        log.info(f"Default user already exists")
        return

    hashed_password = PasswordUtil().hash_password("admin") # TODO change-me: change the default password
    user_create = User(
        user_id=str(uuid.uuid4()),
        username="admin",
        first_name="Admin",
        last_name="User",
        email="admin@localhost.com",
        hashed_password=hashed_password,
        is_active=True,
        roles=["admin"],
        created_by="system",
        created_date=datetime.now(timezone.utc),
        last_updated_by="system",
        last_updated_date=datetime.now(timezone.utc)
    )
    await User.create(user_create)
    log.info(f"Default user initialized")


async def init_migration():
    log.info(f"Initializing migration")
    await init_roles()
    await init_default_user()
    log.info(f"Migration initialized")
