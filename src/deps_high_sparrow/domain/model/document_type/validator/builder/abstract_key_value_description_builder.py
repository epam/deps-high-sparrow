from abc import ABC

from .abstract_list_description_builder import AbstractListDescriptionBuilder
from .abstract_validator_builder import AbstractValidatorBuilder

__all__ = ["AbstractKeyValueDescriptionBuilder"]


class AbstractKeyValueDescriptionBuilder(AbstractListDescriptionBuilder, AbstractValidatorBuilder, ABC):
    def with_key(self) -> "AbstractKeyValueDescriptionBuilder":
        self._add_element_to_parent()

        return self._parent.with_key()

    def with_string_value(self) -> "AbstractKeyValueDescriptionBuilder":
        self._add_element_to_parent()

        return self._parent.with_string_value()

    def with_number_value(self) -> "AbstractKeyValueDescriptionBuilder":
        self._add_element_to_parent()

        return self._parent.with_number_value()

    def with_boolean_value(self) -> "AbstractKeyValueDescriptionBuilder":
        self._add_element_to_parent()

        return self._parent.with_boolean_value()

    def with_range_value(self) -> "AbstractKeyValueDescriptionBuilder":
        self._add_element_to_parent()

        return self._parent.with_range_value()

    def with_date_value(self) -> "AbstractKeyValueDescriptionBuilder":
        self._add_element_to_parent()

        return self._parent.with_date_value()

    def with_time_value(self) -> "AbstractKeyValueDescriptionBuilder":
        self._add_element_to_parent()

        return self._parent.with_time_value()

    def with_datetime_value(self) -> "AbstractKeyValueDescriptionBuilder":
        self._add_element_to_parent()

        return self._parent.with_datetime_value()

    def with_enum_value(self) -> "AbstractKeyValueDescriptionBuilder":
        self._add_element_to_parent()

        return self._parent.with_enum_value()
