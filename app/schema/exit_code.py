from enum import Enum


class ExitCode(str, Enum):
    success = "success"
    fail = "fail"
