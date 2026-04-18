from typing import Any, Callable, Union

from deps_high_sparrow.domain import OperandType, TableDescriptionBuilder
from deps_high_sparrow.domain.exceptions import BusinessException

from ..field_type import FieldType

__all__ = ["BaseTableValidatorCreator"]


class BaseTableValidatorCreator:
    def __init__(self, raw_field: dict[str, Any], builder: TableDescriptionBuilder) -> None:
        self._raw_field = raw_field
        self._is_required = raw_field["required"]
        self._builder = builder

        self._simple_builders: dict[Union[OperandType, FieldType], Callable] = {
            OperandType.NUMBER: self._builder.for_number_column,
            FieldType.CHECKMARK: self._builder.for_boolean_column,
            OperandType.RANGE: self._builder.for_range_column,
            OperandType.TIME: self._builder.for_time_column,
            OperandType.DATETIME: self._builder.for_datetime_column,
            OperandType.STRING: self._builder.for_datetime_column,
        }
        self._builders_with_constraint: dict[OperandType, Callable] = {
            OperandType.DATE: self._add_date_column,
            OperandType.ENUM: self._add_enum_column,
        }

    def _create_columns(self, columns: list[dict[str, Any]]) -> None:
        for index, column in enumerate(columns):
            column_type = column["column_type"]

            if column_type == FieldType.STRING:
                self._add_string_column(index)
            elif column_type in self._simple_builders:
                self._builder = self._simple_builders[column_type](index=index, is_required=self._is_required)
            elif column_type in self._builders_with_constraint:
                self._builders_with_constraint[column_type](index=index, column=column)
            else:
                raise BusinessException(f"Column type `{column_type}` not supported")

    def _add_string_column(self, index: int) -> None:
        # fmt: off
        self._builder = (
            self._builder
            .for_string_column(index=index, is_required=self._is_required)
        )
        # fmt: on

    def _add_date_column(self, index: int, column: dict[str, Any]) -> None:
        self._builder = self._builder.for_date_column(
            index=index,
            is_required=self._is_required,
        )

        if column_constraint := column.get("column_data"):
            self._builder = self._builder.with_format(column_constraint["format"])

    def _add_enum_column(self, index: int, column: dict[str, Any]) -> None:
        self._builder = self._builder.for_enum_column(
            index=index,
            is_required=self._is_required,
        )

        if column_constraint := column.get("column_data"):
            self._builder = self._builder.with_options(column_constraint["options"])
