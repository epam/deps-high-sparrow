from dataclasses import dataclass
from dataclasses import field as dataclass_field
from typing import Any, List, Optional, Tuple, Union

from ..entities.constants import OperandType
from .field import (
    ArrayFieldTypeMeta,
    BasicFieldTypeMeta,
    DateFieldTypeMeta,
    DictFieldTypeMeta,
    EnumFieldTypeMeta,
    StringFieldTypeMeta,
    TableFieldTypeMeta,
)


@dataclass
class BaseDataToValidate:
    document_id: int
    field_code: str
    document_type_code: str
    field_type: OperandType
    meta: Any
    data: Any
    is_required: bool


@dataclass
class BaseData:
    value: Any


@dataclass
class Coordinates:
    column: int
    row: int


@dataclass
class Cell(BaseData):
    coordinates: Coordinates


@dataclass
class TableData:
    cells: List[Cell] = dataclass_field(default_factory=list)


@dataclass
class FieldDataToValidate(BaseDataToValidate):
    meta: Union[
        BasicFieldTypeMeta,
        StringFieldTypeMeta,
        EnumFieldTypeMeta,
        DateFieldTypeMeta,
    ]
    data: BaseData
    is_required: bool = True


@dataclass
class TableDataToValidate(BaseDataToValidate):
    meta: TableFieldTypeMeta
    data: TableData
    is_required: bool = True
    is_size_valid: Optional[bool] = None
    is_column_size_correct: bool = True


@dataclass
class DictData:
    items: Tuple[FieldDataToValidate, FieldDataToValidate]


@dataclass
class DictDataToValidate(BaseDataToValidate):
    meta: DictFieldTypeMeta
    is_required: bool = True
    data: DictData


@dataclass
class ArrayData:
    items: Union[List[TableDataToValidate], List[FieldDataToValidate], List[DictDataToValidate]]


@dataclass
class ArrayDataToValidate(BaseDataToValidate):
    meta: ArrayFieldTypeMeta
    data: ArrayData
    is_required: bool = True
