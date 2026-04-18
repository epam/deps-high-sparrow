from typing import Any, Optional

from ...operand_type import OperandType
from ..description import GenericDescription, ListDescription
from .abstract_list_description_builder import AbstractListDescriptionBuilder
from .generic_description_builder import GenericDescriptionBuilder
from .key_value_description_builder import KeyValueDescriptionBuilder
from .table_description_builder import TableDescriptionBuilder

__all__ = ["ListDescriptionBuilder"]


class ListDescriptionBuilder(AbstractListDescriptionBuilder):
    def __init__(self, *, parent: Optional[Any] = None):
        super().__init__(parent=parent)

        self._type: Optional[OperandType] = None
        self._description: Optional[GenericDescription] = None

    def for_string_item(self) -> GenericDescriptionBuilder:
        self._type = OperandType.STRING

        return self._GenericItemDescriptionBuilder(type=OperandType.STRING, parent=self)

    def for_number_item(self) -> GenericDescriptionBuilder:
        self._type = OperandType.NUMBER

        return self._GenericItemDescriptionBuilder(type=OperandType.NUMBER, parent=self)

    def for_boolean_item(self) -> GenericDescriptionBuilder:
        self._type = OperandType.BOOL

        return self._GenericItemDescriptionBuilder(type=OperandType.BOOL, parent=self)

    def for_range_item(self) -> GenericDescriptionBuilder:
        self._type = OperandType.RANGE

        return self._GenericItemDescriptionBuilder(type=OperandType.RANGE, parent=self)

    def for_date_item(self) -> GenericDescriptionBuilder:
        self._type = OperandType.DATE

        return self._GenericItemDescriptionBuilder(type=OperandType.DATE, parent=self)

    def for_time_item(self) -> GenericDescriptionBuilder:
        self._type = OperandType.TIME

        return self._GenericItemDescriptionBuilder(type=OperandType.TIME, parent=self)

    def for_datetime_item(self) -> GenericDescriptionBuilder:
        self._type = OperandType.DATETIME

        return self._GenericItemDescriptionBuilder(type=OperandType.DATETIME, parent=self)

    def for_enum_item(self) -> GenericDescriptionBuilder:
        self._type = OperandType.ENUM

        return self._GenericItemDescriptionBuilder(type=OperandType.ENUM, parent=self)

    def for_key_value_item(self) -> KeyValueDescriptionBuilder:
        self._type = OperandType.DICT

        return self._KeyValueItemDescriptionBuilder(parent=self)

    def for_table_item(self) -> TableDescriptionBuilder:
        self._type = OperandType.TABLE

        return self._TableItemDescriptionBuilder(parent=self)

    def _build(self) -> ListDescription:
        return ListDescription(item_type=self._type, meta=self._description)

    class _GenericItemDescriptionBuilder(GenericDescriptionBuilder):
        def _add_to_parent(self) -> None:
            self._parent._description = self._build()

    class _KeyValueItemDescriptionBuilder(KeyValueDescriptionBuilder):
        def _add_to_parent(self) -> None:
            self._parent._description = self._build()

    class _TableItemDescriptionBuilder(TableDescriptionBuilder):
        def _add_to_parent(self) -> None:
            self._parent._description = self._build()
