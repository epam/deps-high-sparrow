from typing import Any, Callable, Union

from deps_high_sparrow.domain import OperandType
from deps_high_sparrow.domain.exceptions.base import BusinessException
from deps_high_sparrow.domain.model import KeyValueDescriptionBuilder

from ..field_type import FieldType

__all__ = ["BaseKVPValidatorCreator"]


class BaseKVPValidatorCreator:
    def __init__(self, raw_field: dict[str, Any], builder: KeyValueDescriptionBuilder) -> None:
        self._raw_field = raw_field
        self._builder = builder

        self._simple_builders: dict[Union[OperandType, FieldType], Callable] = {
            OperandType.NUMBER: self._builder.with_number_value,
            FieldType.CHECKMARK: self._builder.with_boolean_value,
            OperandType.RANGE: self._builder.with_range_value,
            OperandType.TIME: self._builder.with_time_value,
            OperandType.DATETIME: self._builder.with_datetime_value,
        }
        self._builders_with_constraint: dict[OperandType, Callable] = {
            OperandType.DATE: self._add_date_value,
            OperandType.ENUM: self._add_enum_value,
        }

    def _create_key_value_pair(self, field_constraint: dict[str, Any]) -> None:
        self._builder = self._builder.with_key()

        base_type = field_constraint["value_type"]

        if base_type == OperandType.STRING:
            self._add_string_value()
        elif base_type in self._simple_builders:
            self._builder = self._simple_builders[base_type]()
        elif base_type in self._builders_with_constraint:
            self._builders_with_constraint[base_type](field_constraint)
        else:
            raise BusinessException(f"Key value pair item type `{base_type}` not supported")

    def _add_string_value(self):
        self._builder = self._builder.with_string_value()

    def _add_date_value(self, constraint: dict[str, Any]) -> None:
        self._builder = self._builder.with_date_value()

        if value_constraint := constraint.get("value_data"):
            self._builder = self._builder.with_format(value_constraint["format"])

    def _add_enum_value(self, constraint: dict[str, Any]) -> None:
        self._builder = self._builder.with_enum_value()

        if value_constraint := constraint.get("value_data"):
            self._builder = self._builder.with_options(value_constraint["options"])
