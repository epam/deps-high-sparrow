from typing import Any, Optional

from ...operand_type import OperandType
from ..description import (
    BasicDescription,
    DateDescription,
    EnumDescription,
    GenericDescription,
    StringDescription,
)
from .abstract_generic_description_builder import AbstractGenericDescriptionBuilder

__all__ = ["GenericDescriptionBuilder"]


class GenericDescriptionBuilder(AbstractGenericDescriptionBuilder):
    def __init__(self, *, type: OperandType, parent: Optional[Any] = None) -> None:
        super().__init__(parent=parent)
        self._type = type
        self._basic_types: set[OperandType] = {
            OperandType.NUMBER,
            OperandType.BOOL,
            OperandType.RANGE,
            OperandType.DATETIME,
            OperandType.TIME,
        }

        self._allowed_values: Optional[list[str]] = None
        self._restricted_values: Optional[list[str]] = None

        self._options: Optional[list[str]] = None

        self._format: Optional[str] = None

    def with_restrictions(self, allowed_values: list[str], restricted_values: list[str]) -> "GenericDescriptionBuilder":
        self._allowed_values = allowed_values
        self._restricted_values = restricted_values

        return self

    def with_options(self, options: list[str]) -> "GenericDescriptionBuilder":
        self._options = options

        return self

    def with_format(self, format: str) -> "GenericDescriptionBuilder":
        self._format = format

        return self

    def _add_to_parent(self) -> None:
        pass

    def _build(self) -> GenericDescription:
        if self._type in self._basic_types:
            return BasicDescription(
                allowed_values=self._allowed_values,
                restricted_values=self._restricted_values,
            )

        if self._type == OperandType.STRING:
            return StringDescription()

        if self._type == OperandType.ENUM and self._options is not None:
            return EnumDescription(options=self._options)

        if self._type == OperandType.DATE and self._format is not None:
            return DateDescription(format=self._format)

        return BasicDescription()
