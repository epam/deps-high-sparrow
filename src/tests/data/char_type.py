from enum import Enum

__all__ = ["CharType"]


class CharType(str, Enum):
    NUMERIC = "numeric"
    ALPHABETIC = "alphabetic"
    ALPHANUMERIC = "alphanumeric"
    BOOLEAN = "boolean"
