from enum import Enum


class Severity(Enum):
    WARNING = "warning"
    ERROR = "error"


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


BASIC_TYPES = (
    OperandType.STRING,
    OperandType.NUMBER,
    OperandType.BOOL,
    OperandType.RANGE,
    OperandType.DATE,
    OperandType.TIME,
    OperandType.DATETIME,
)


class KeyValueId(str, Enum):
    KEY = "key"
    VALUE = "value"


DICT_ITEMS = (KeyValueId.KEY, KeyValueId.VALUE)
