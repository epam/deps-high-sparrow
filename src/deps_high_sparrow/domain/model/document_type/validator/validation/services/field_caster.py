from collections import defaultdict
from typing import Any, Callable, DefaultDict, List, Optional, Tuple

from ..dto.field import DictFieldTypeMeta, TableFieldTypeMeta
from ..dto.prepared_field import BaseDataToValidate, Cell
from ..entities.constants import BASIC_TYPES, OperandType
from ..interfaces import IFieldCasterService
from .utils import cast_field, has_value


class FieldCasterService(IFieldCasterService):
    def __init__(self):
        self._type_cast_mapper: DefaultDict[OperandType, Tuple[Callable, str]] = defaultdict(
            lambda: (self.cast, "value")
        )
        self._type_cast_mapper.update(
            {
                OperandType.TABLE: (self.cast_table, "cells"),
                OperandType.ARRAY: (self.cast_array, "items"),
                OperandType.ENUM: (lambda value, *args, meta: value, "value"),
                OperandType.DICT: (self.cast_dict, "items"),
            }
        )

    def cast(
        self,
        value: Any,
        field_type: OperandType,
        meta: Optional[Any] = None,
    ):
        if field_type in BASIC_TYPES:
            return cast_field(value, field_type)

        return self.cast_array(items=value)  # type: ignore

    def cast_array(self, items: List[BaseDataToValidate], *args, **kwargs):
        self.cast_field_values(items)
        return items

    def cast_table(self, cells: List[Cell], *_, meta: TableFieldTypeMeta):
        for column_meta in meta.columns:  # noqa: WPS426
            column_cells = filter(lambda cell: cell.coordinates.column == column_meta.index, cells)
            for local_cell in column_cells:
                if has_value(local_cell.value):
                    cast_function = self._type_cast_mapper[column_meta.item_type][0]
                    local_cell.value = cast_function(local_cell.value, column_meta.item_type, meta=column_meta.meta)

        return cells

    def cast_dict(
        self,
        items: Tuple[BaseDataToValidate, BaseDataToValidate],
        field_type: OperandType,
        meta: Optional[DictFieldTypeMeta] = None,
    ):
        casted_key, casted_value = self.cast_field_values([items[0], items[1]])
        return (casted_key, casted_value)  # noqa: WPS331

    def cast_field_values(self, fields: List[BaseDataToValidate]) -> List[BaseDataToValidate]:
        for field in fields:
            cast_function, attribute = self._type_cast_mapper[field.field_type]
            value = getattr(field.data, attribute, None)
            if has_value(value):
                casted_value = cast_function(value, field.field_type, meta=field.meta)
                setattr(field.data, attribute, casted_value)

        return fields

    def cast_field(self, field: BaseDataToValidate) -> BaseDataToValidate:
        cast_function, attribute = self._type_cast_mapper[field.field_type]
        value = getattr(field.data, attribute, None)
        if has_value(value):
            casted_value = cast_function(value, field.field_type, meta=field.meta)
            setattr(field.data, attribute, casted_value)

        return field
