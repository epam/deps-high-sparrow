from typing import Any, Optional

from ...operand_type import OperandType
from ..description import ColumnDescription, GenericDescription, TableDescription
from .abstract_table_description_builder import AbstractTableDescriptionBuilder
from .generic_description_builder import GenericDescriptionBuilder

__all__ = ["TableDescriptionBuilder"]


class TableDescriptionBuilder(AbstractTableDescriptionBuilder):
    def __init__(self, *, parent: Optional[Any] = None):
        super().__init__(parent=parent)

        self._index: Optional[int] = None
        self._is_required: Optional[bool] = None
        self._type: Optional[OperandType] = None
        self._description: Optional[GenericDescription] = None

        self._columns: list[ColumnDescription] = []

    def for_string_column(self, index: int, is_required: bool) -> GenericDescriptionBuilder:
        self._add_column_description()
        self._index = index
        self._is_required = is_required
        self._type = OperandType.STRING

        return self._ColumnDescriptionBuilder(type=OperandType.STRING, parent=self)

    def for_number_column(self, index: int, is_required: bool) -> GenericDescriptionBuilder:
        self._add_column_description()
        self._index = index
        self._is_required = is_required
        self._type = OperandType.NUMBER

        return self._ColumnDescriptionBuilder(type=OperandType.NUMBER, parent=self)

    def for_boolean_column(self, index: int, is_required: bool) -> GenericDescriptionBuilder:
        self._add_column_description()
        self._index = index
        self._is_required = is_required
        self._type = OperandType.BOOL

        return self._ColumnDescriptionBuilder(type=OperandType.BOOL, parent=self)

    def for_range_column(self, index: int, is_required: bool) -> GenericDescriptionBuilder:
        self._add_column_description()
        self._index = index
        self._is_required = is_required
        self._type = OperandType.RANGE

        return self._ColumnDescriptionBuilder(type=OperandType.RANGE, parent=self)

    def for_date_column(self, index: int, is_required: bool) -> GenericDescriptionBuilder:
        self._add_column_description()
        self._index = index
        self._is_required = is_required
        self._type = OperandType.DATE

        return self._ColumnDescriptionBuilder(type=OperandType.DATE, parent=self)

    def for_time_column(self, index: int, is_required: bool) -> GenericDescriptionBuilder:
        self._add_column_description()
        self._index = index
        self._is_required = is_required
        self._type = OperandType.TIME

        return self._ColumnDescriptionBuilder(type=OperandType.TIME, parent=self)

    def for_datetime_column(self, index: int, is_required: bool) -> GenericDescriptionBuilder:
        self._add_column_description()
        self._index = index
        self._is_required = is_required
        self._type = OperandType.DATETIME

        return self._ColumnDescriptionBuilder(type=OperandType.DATETIME, parent=self)

    def for_enum_column(self, index: int, is_required: bool) -> GenericDescriptionBuilder:
        self._add_column_description()
        self._index = index
        self._is_required = is_required
        self._type = OperandType.ENUM

        return self._ColumnDescriptionBuilder(type=OperandType.ENUM, parent=self)

    def _add_column_description(self) -> None:
        if self._index is not None and self._is_required is not None and self._type is not None:
            self._columns.append(
                ColumnDescription(
                    index=self._index,
                    is_required=self._is_required,
                    item_type=self._type,
                    meta=self._description,
                )
            )
            self._index, self._is_required, self._type = None, None, None

    def _build(self) -> TableDescription:
        self._add_column_description()
        return TableDescription(columns=self._columns)

    class _ColumnDescriptionBuilder(GenericDescriptionBuilder):
        def _add_to_parent(self) -> None:
            self._parent._description = self._build()
