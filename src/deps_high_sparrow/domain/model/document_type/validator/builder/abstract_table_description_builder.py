from abc import ABC

from .abstract_list_description_builder import AbstractListDescriptionBuilder
from .abstract_validator_builder import AbstractValidatorBuilder

__all__ = ["AbstractTableDescriptionBuilder"]


class AbstractTableDescriptionBuilder(AbstractListDescriptionBuilder, AbstractValidatorBuilder, ABC):
    def for_string_column(self, index: int, is_required: bool) -> "AbstractTableDescriptionBuilder":
        self._add_element_to_parent()

        return self._parent.for_string_column(index, is_required)

    def for_number_column(self, index: int, is_required: bool) -> "AbstractTableDescriptionBuilder":
        self._add_element_to_parent()

        return self._parent.for_number_column(index, is_required)

    def for_boolean_column(self, index: int, is_required: bool) -> "AbstractTableDescriptionBuilder":
        self._add_element_to_parent()

        return self._parent.for_boolean_column(index, is_required)

    def for_range_column(self, index: int, is_required: bool) -> "AbstractTableDescriptionBuilder":
        self._add_element_to_parent()

        return self._parent.for_range_column(index, is_required)

    def for_date_column(self, index: int, is_required: bool) -> "AbstractTableDescriptionBuilder":
        self._add_element_to_parent()

        return self._parent.for_date_column(index, is_required)

    def for_time_column(self, index: int, is_required: bool) -> "AbstractTableDescriptionBuilder":
        self._add_element_to_parent()

        return self._parent.for_time_column(index, is_required)

    def for_datetime_column(self, index: int, is_required: bool) -> "AbstractTableDescriptionBuilder":
        self._add_element_to_parent()

        return self._parent.for_datetime_column(index, is_required)

    def for_enum_column(self, index: int, is_required: bool) -> "AbstractTableDescriptionBuilder":
        self._add_element_to_parent()

        return self._parent.for_enum_column(index, is_required)
