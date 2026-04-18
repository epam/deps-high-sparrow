from enum import Enum

__all__ = ["FieldType"]


class FieldType(str, Enum):
    TABLE = "table"
    STRING = "string"
    CHECKMARK = "checkmark"
    LIST = "list"
    DICT = "dict"
    ENUM = "enum"
    DATE = "date"
