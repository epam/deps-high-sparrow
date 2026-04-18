from enum import Enum

__all__ = ["Severity"]


class Severity(Enum):
    WARNING = "warning"
    ERROR = "error"
