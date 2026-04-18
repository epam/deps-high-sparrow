import logging
from typing import Any, Callable, Mapping, Union

from deps_high_sparrow.domain import DocumentType, OperandType
from deps_high_sparrow.domain.exceptions.base import BusinessException

from .field_type import FieldType
from .key_value_pair import KVPValidatorCreator
from .list import ListValidatorCreator
from .table import TableValidatorCreator

__all__ = ["ValidatorCreator"]


class ValidatorCreator:
    def __init__(self, document_type: DocumentType) -> None:
        self._document_type = document_type

        self._creators: dict[Union[OperandType, FieldType], Callable] = {
            OperandType.STRING: self._create_string,
            OperandType.DATE: self._create_date,
            OperandType.ENUM: self._create_enum,
            OperandType.NUMBER: self._create_basic,
            OperandType.RANGE: self._create_basic,
            OperandType.TIME: self._create_basic,
            OperandType.DATETIME: self._create_basic,
            OperandType.TABLE: self._create_table,
            OperandType.DICT: self._create_dict,
            FieldType.LIST: self._create_list,
            FieldType.CHECKMARK: self._create_basic,
        }

        self._logger = logging.getLogger(self.__class__.__name__)

    def create_for_field(self, raw_field: Mapping[str, Any]) -> None:
        field_type = raw_field["field_type"]
        if creator := self._creators.get(field_type):
            creator(raw_field)
        else:
            raise BusinessException(f"Couldn't create field `{raw_field}`. Field type {field_type} not supported...")

    def create_for_fields(self, raw_fields: list[dict[str, Any]]) -> None:
        for raw_field in raw_fields:
            self.create_for_field(raw_field)

    def _create_string(self, raw_field: dict[str, Any]) -> None:
        builder = self._document_type.add_string_validator(raw_field["code"]).with_description()

        if raw_field["required"]:
            builder = builder.is_required()

        builder.build()

    def _create_date(self, raw_field: dict[str, Any]) -> None:
        builder = self._document_type.add_date_validator(raw_field["code"]).with_description()

        if field_constraint := raw_field.get("field_data"):
            builder = builder.with_format(field_constraint["format"])

        if raw_field["required"]:
            builder = builder.is_required()

        builder.build()

    def _create_enum(self, raw_field: dict[str, Any]) -> None:
        builder = self._document_type.add_enum_validator(raw_field["code"]).with_description()

        if field_constraint := raw_field.get("field_data"):
            builder = builder.with_options(field_constraint["options"])

        if raw_field["required"]:
            builder = builder.is_required()

        builder.build()

    def _create_basic(self, raw_field: dict[str, Any]) -> None:
        basic_builders: dict[Union[OperandType, FieldType], Callable] = {
            FieldType.CHECKMARK: self._document_type.add_boolean_validator,
            OperandType.NUMBER: self._document_type.add_number_validator,
            OperandType.RANGE: self._document_type.add_range_validator,
            OperandType.TIME: self._document_type.add_time_validator,
            OperandType.DATETIME: self._document_type.add_datetime_validator,
        }

        builder = basic_builders[raw_field["field_type"]](raw_field["code"]).with_description()

        if raw_field["required"]:
            builder = builder.is_required()

        builder.build()

    def _create_table(self, raw_field: dict[str, Any]) -> None:
        TableValidatorCreator(document_type=self._document_type, raw_field=raw_field).create()

    def _create_list(self, raw_field: dict[str, Any]) -> None:
        ListValidatorCreator(document_type=self._document_type, raw_field=raw_field).create()

    def _create_dict(self, raw_field: dict[str, Any]) -> None:
        KVPValidatorCreator(document_type=self._document_type, raw_field=raw_field).create()
