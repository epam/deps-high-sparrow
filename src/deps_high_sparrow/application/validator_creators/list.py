import logging
from typing import Any, Callable, Union

from deps_high_sparrow.domain import DocumentType, OperandType
from deps_high_sparrow.domain.exceptions.base import BusinessException

from .field_type import FieldType
from .key_value_pair import ListKVPValidatorCreator
from .table import ListTableValidatorCreator

__all__ = ["ListValidatorCreator"]


class ListValidatorCreator:
    def __init__(self, document_type: DocumentType, raw_field: dict[str, Any]) -> None:
        self._raw_field = raw_field
        self._is_required = self._raw_field["required"]
        self._builder = document_type.add_list_validator(self._raw_field["code"]).with_description()

        self._simple_builders: dict[Union[OperandType, FieldType], Callable] = {
            OperandType.NUMBER: self._builder.for_number_item,
            FieldType.CHECKMARK: self._builder.for_boolean_item,
            OperandType.RANGE: self._builder.for_range_item,
            OperandType.TIME: self._builder.for_time_item,
            OperandType.DATETIME: self._builder.for_datetime_item,
        }
        self._builders_with_constraint: dict[OperandType, Callable] = {
            OperandType.DATE: self._add_date_item,
            OperandType.ENUM: self._add_enum_item,
            OperandType.TABLE: self._add_table_item,
            OperandType.DICT: self._add_key_value_pair_item,
        }

        self._logger = logging.getLogger(self.__class__.__name__)

    def create(self) -> None:
        if field_constraint := self._raw_field.get("field_data"):
            self._set_item_constraint(field_constraint)

            if self._is_required:
                self._builder = self._builder.is_required()

            self._builder.build()

        else:
            self._logger.warning(
                "Cannot create validator for `%s` document_type. Reason: field `%s` without field constraint",
                self._raw_field.get("document_type_id"),
                self._raw_field.get("code"),
            )

    def _set_item_constraint(self, item_constraint: dict[str, Any]) -> None:
        base_type = item_constraint["base_type"]

        if base_type == OperandType.STRING:
            self._add_string_item()
        elif base_type in self._simple_builders:
            self._builder = self._simple_builders[base_type]()
        elif base_type in self._builders_with_constraint:
            self._builders_with_constraint[base_type](item_constraint["base_type_data"])
        else:
            raise BusinessException(f"List item type `{base_type}` not supported")

    def _add_string_item(self) -> None:
        self._builder = self._builder.for_string_item()

    def _add_date_item(self, constraint: dict[str, Any]) -> None:
        self._builder = self._builder.for_date_item().with_format(constraint["format"])

    def _add_enum_item(self, constraint: dict[str, Any]) -> None:
        self._builder = self._builder.for_enum_item().with_options(constraint["options"])

    def _add_table_item(self, constraint: dict[str, Any]) -> None:
        creator = ListTableValidatorCreator(raw_field=self._raw_field, builder=self._builder.for_table_item())
        self._builder = creator.create_columns(constraint["columns"])

    def _add_key_value_pair_item(self, constraint: dict[str, Any]) -> None:
        creator = ListKVPValidatorCreator(raw_field=self._raw_field, builder=self._builder.for_key_value_item())
        self._builder = creator.create_key_value_pair(constraint)
