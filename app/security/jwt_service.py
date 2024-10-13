import logging

log = logging.getLogger(__name__)


class JWTToken:
    def __init__(self, id_token: str):
        self.id_token = id_token


class JWTService:
    pass
