from abc import ABC

from .abstract_key_value_description_builder import AbstractKeyValueDescriptionBuilder
from .abstract_list_description_builder import AbstractListDescriptionBuilder
from .abstract_table_description_builder import AbstractTableDescriptionBuilder
from .abstract_validator_builder import AbstractValidatorBuilder

__all__ = ["AbstractGenericDescriptionBuilder"]


class AbstractGenericDescriptionBuilder(
    AbstractKeyValueDescriptionBuilder,
    AbstractTableDescriptionBuilder,
    AbstractListDescriptionBuilder,
    AbstractValidatorBuilder,
    ABC,
):
    def with_restrictions(
        self, allowed_values: list[str], restricted_values: list[str]
    ) -> "AbstractGenericDescriptionBuilder":
        self._add_element_to_parent()

        return self._parent.with_restrictions(allowed_values, restricted_values)

    def with_options(self, options: int) -> "AbstractGenericDescriptionBuilder":
        self._add_element_to_parent()

        return self._parent.with_options(options)

    def with_format(self, format: int) -> "AbstractGenericDescriptionBuilder":
        self._add_element_to_parent()

        return self._parent.with_format(format)
