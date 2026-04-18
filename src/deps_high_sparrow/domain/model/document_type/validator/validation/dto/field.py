from collections import defaultdict
from dataclasses import asdict, dataclass, field
from typing import Any, Callable, DefaultDict, List, Optional, Union

from ..entities.constants import OperandType


class _PostInitData:
    meta: Any
    item_type: Any

    def __post_init__(self):
        mapper: DefaultDict[OperandType, Callable] = defaultdict(lambda: BasicFieldTypeMeta)
        mapper.update(
            {
                OperandType.STRING: StringFieldTypeMeta,
                OperandType.ENUM: EnumFieldTypeMeta,
                OperandType.TABLE: TableFieldTypeMeta,
                OperandType.DICT: DictFieldTypeMeta,
            }
        )

        if isinstance(self.meta, dict):
            meta_type = mapper[self.item_type]
            self.meta = meta_type(**self.meta)


@dataclass
class FieldCodeAndDocumentType:
    field_code: str
    document_type_code: str


@dataclass
class BasicFieldTypeMeta:
    allowed_values: List[Any] = field(default_factory=list)
    restricted_values: List[Any] = field(default_factory=list)
    field_name: Optional[str] = None

    def as_dict(self):
        return asdict(self)


@dataclass
class StringFieldTypeMeta:
    pass  # noqa: WPS604

    def as_dict(self):
        return asdict(self)


@dataclass
class EnumFieldTypeMeta:
    options: List[Any]

    def as_dict(self):
        return asdict(self)


@dataclass
class DateFieldTypeMeta:
    format: str

    def as_dict(self):
        return asdict(self)


@dataclass
class ColumnTypeMeta(_PostInitData):
    index: int
    is_required: bool
    item_type: OperandType
    meta: Union[StringFieldTypeMeta, EnumFieldTypeMeta, BasicFieldTypeMeta]

    def as_dict(self):
        ctm_dict = asdict(self)
        ctm_dict.update(item_type=self.item_type.value, meta=asdict(self.meta))
        return ctm_dict


@dataclass
class TableFieldTypeMeta:
    columns: List[ColumnTypeMeta]

    def __post_init__(self):
        self.columns = [ColumnTypeMeta(**column) if isinstance(column, dict) else column for column in self.columns]

    def as_dict(self):
        return {"columns": [column.as_dict() for column in self.columns]}


@dataclass
class DictFieldTypeMeta:
    key_type: OperandType
    key_meta: Union[StringFieldTypeMeta, BasicFieldTypeMeta]
    value_type: OperandType
    value_meta: Union[StringFieldTypeMeta, BasicFieldTypeMeta]

    def __post_init__(self):
        if isinstance(self.key_meta, dict):
            self.key_meta = (
                StringFieldTypeMeta(**self.key_meta)
                if self.key_type == OperandType.STRING
                else BasicFieldTypeMeta(**self.key_meta)
            )
        if isinstance(self.value_meta, dict):
            self.value_meta = (
                StringFieldTypeMeta(**self.value_meta)
                if self.value_type == OperandType.STRING
                else BasicFieldTypeMeta(**self.value_meta)
            )

    def as_dict(self):
        return {
            "key_type": self.key_type.value,
            "key_meta": self.key_meta.as_dict(),
            "value_type": self.value_type.value,
            "value_meta": self.value_meta.as_dict(),
        }


@dataclass
class ArrayFieldTypeMeta(_PostInitData):
    item_type: OperandType
    meta: Union[
        StringFieldTypeMeta,
        EnumFieldTypeMeta,
        TableFieldTypeMeta,
        BasicFieldTypeMeta,
        DictFieldTypeMeta,
    ]
    field_name: Optional[str] = None

    def as_dict(self):
        return {
            "item_type": self.item_type.value,
            "meta": self.meta.as_dict(),
            "field_name": self.field_name,
        }


FieldMetaType = Union[
    DateFieldTypeMeta,
    BasicFieldTypeMeta,
    ArrayFieldTypeMeta,
    StringFieldTypeMeta,
    TableFieldTypeMeta,
    EnumFieldTypeMeta,
    DictFieldTypeMeta,
]
