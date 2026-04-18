from enum import Enum

__all__ = ["OperandType"]


class OperandType(str, Enum):
    STRING = "string"
    NUMBER = "number"  # float
    BOOL = "bool"
    ARRAY = "array"
    RANGE = "range"
    DATE = "date"
    TIME = "time"
    DATETIME = "datetime"
    ENUM = "enum"
    FIELD = "field"
    TABLE = "table"
    DICT = "dict"
