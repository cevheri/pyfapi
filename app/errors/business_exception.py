from enum import Enum


class ErrorCodes(Enum):
    """
    Error codes for business exceptions
    """
    UNAUTHORIZED = "UNAUTHORIZED"
    ALREADY_EXISTS = "ALREADY_EXISTS"
    MESSAGE_SAVE_ERROR = "MESSAGE_SAVE_ERROR"
    NOT_FOUND = "NOT_FOUND"
    INVALID_PAYLOAD = "INVALID_PAYLOAD"
    INVALID_INPUT = "INVALID_INPUT"
    INVALID_OPERATION = "INVALID_OPERATION"
    INVALID_STATE = "INVALID_STATE"
    FORBIDDEN = "FORBIDDEN"
    CONFLICT = "CONFLICT"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"


class BusinessException(Exception):
    def __init__(self, code: ErrorCodes, msg: str):
        self.code = code
        self.msg = msg
        super().__init__(msg)
