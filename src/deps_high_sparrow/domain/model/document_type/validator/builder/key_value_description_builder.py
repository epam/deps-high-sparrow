from typing import Any, Optional

from ...operand_type import OperandType
from ..description import GenericDescription, KeyValueDescription
from .abstract_key_value_description_builder import AbstractKeyValueDescriptionBuilder
from .generic_description_builder import GenericDescriptionBuilder

__all__ = ["KeyValueDescriptionBuilder"]


class KeyValueDescriptionBuilder(AbstractKeyValueDescriptionBuilder):
    def __init__(self, *, parent: Optional[Any] = None):
        super().__init__(parent=parent)

        self._key_type = OperandType.STRING
        self._key_description: Optional[GenericDescription] = None

        self._value_type: Optional[OperandType] = None
        self._value_description: Optional[GenericDescription] = None

    def with_key(self) -> GenericDescriptionBuilder:
        return self._KeyDescriptionBuilder(type=OperandType.STRING, parent=self)

    def with_string_value(self) -> GenericDescriptionBuilder:
        self._value_type = OperandType.STRING

        return self._ValueDescriptionBuilder(type=OperandType.STRING, parent=self)

    def with_number_value(self) -> GenericDescriptionBuilder:
        self._value_type = OperandType.NUMBER

        return self._ValueDescriptionBuilder(type=OperandType.NUMBER, parent=self)

    def with_boolean_value(self) -> GenericDescriptionBuilder:
        self._value_type = OperandType.BOOL

        return self._ValueDescriptionBuilder(type=OperandType.BOOL, parent=self)

    def with_range_value(self) -> GenericDescriptionBuilder:
        self._value_type = OperandType.RANGE

        return self._ValueDescriptionBuilder(type=OperandType.RANGE, parent=self)

    def with_date_value(self) -> GenericDescriptionBuilder:
        self._value_type = OperandType.DATE

        return self._ValueDescriptionBuilder(type=OperandType.DATE, parent=self)

    def with_time_value(self) -> GenericDescriptionBuilder:
        self._value_type = OperandType.TIME

        return self._ValueDescriptionBuilder(type=OperandType.TIME, parent=self)

    def with_datetime_value(self) -> GenericDescriptionBuilder:
        self._value_type = OperandType.DATETIME

        return self._ValueDescriptionBuilder(type=OperandType.DATETIME, parent=self)

    def with_enum_value(self) -> GenericDescriptionBuilder:
        self._value_type = OperandType.ENUM

        return self._ValueDescriptionBuilder(type=OperandType.ENUM, parent=self)

    def _build(self) -> KeyValueDescription:
        return KeyValueDescription(
            key_type=self._key_type,
            key_meta=self._key_description,
            value_type=self._value_type,
            value_meta=self._value_description,
        )

    class _KeyDescriptionBuilder(GenericDescriptionBuilder):
        def _add_to_parent(self) -> None:
            self._parent._key_description = self._build()

    class _ValueDescriptionBuilder(GenericDescriptionBuilder):
        def _add_to_parent(self) -> None:
            self._parent._value_description = self._build()
