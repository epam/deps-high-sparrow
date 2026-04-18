from abc import ABC

from .abstract_validator_builder import AbstractValidatorBuilder

__all__ = ["AbstractListDescriptionBuilder"]


class AbstractListDescriptionBuilder(AbstractValidatorBuilder, ABC):
    def for_string_item(self) -> "AbstractListDescriptionBuilder":
        self._add_element_to_parent()

        return self._parent.for_string_item()

    def for_number_item(self) -> "AbstractListDescriptionBuilder":
        self._add_element_to_parent()

        return self._parent.for_number_item()

    def for_boolean_item(self) -> "AbstractListDescriptionBuilder":
        self._add_element_to_parent()

        return self._parent.for_boolean_item()

    def for_range_item(self) -> "AbstractListDescriptionBuilder":
        self._add_element_to_parent()

        return self._parent.for_range_item()

    def for_date_item(self) -> "AbstractListDescriptionBuilder":
        self._add_element_to_parent()

        return self._parent.for_date_item()

    def for_time_item(self) -> "AbstractListDescriptionBuilder":
        self._add_element_to_parent()

        return self._parent.for_time_item()

    def for_datetime_item(self) -> "AbstractListDescriptionBuilder":
        self._add_element_to_parent()

        return self._parent.for_datetime_item()

    def for_enum_item(self) -> "AbstractListDescriptionBuilder":
        self._add_element_to_parent()

        return self._parent.for_enum_item()

    def for_key_value_item(self) -> "AbstractListDescriptionBuilder":
        self._add_element_to_parent()

        return self._parent.for_key_value_item()
