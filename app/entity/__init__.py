# Declare the entities that will be imported when importing the package

import logging

from app.entity.role_entity import Role
from app.entity.user_entity import User

db_entities = [User, Role]
log = logging.getLogger(__name__)


def __all__():
    log.info(f"Importing db entities names: {[entity.__name__ for entity in db_entities]}")
    return db_entities
