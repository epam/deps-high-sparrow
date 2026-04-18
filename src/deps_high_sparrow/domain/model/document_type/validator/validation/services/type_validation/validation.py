import logging
from collections import defaultdict
from datetime import date, datetime
from typing import Any, Callable, DefaultDict, Dict, List, Union

from ......validation_result import Issues
from ...dto.field import (
    ArrayFieldTypeMeta,
    BasicFieldTypeMeta,
    DateFieldTypeMeta,
    EnumFieldTypeMeta,
    StringFieldTypeMeta,
)
from ...dto.prepared_field import (
    ArrayDataToValidate,
    BaseDataToValidate,
    DictDataToValidate,
    FieldDataToValidate,
    TableDataToValidate,
)
from ...dto.validation import ValidationResultDTO
from ...entities.constants import DICT_ITEMS, OperandType
from ...exceptions import InvalidType
from ...interfaces import IValidationService
from ..utils import FieldValidationIssues, Message, add_error_marker, has_value
from .constants import DATE_FORMATS

logger = logging.getLogger(__name__)


# noinspection PyUnusedLocal
class TypeValidationService(IValidationService):
    NUMBER_LOWER_BOUNDARY = -999999999999.999999
    NUMBER_UPPER_BOUNDARY = 999999999999.999999

    DATE_LOWER_BOUNDARY = date(1900, 1, 1)  # noqa: WPS432
    DATE_UPPER_BOUNDARY = date(2099, 12, 31)  # noqa: WPS432

    def __init__(self):
        self._base_data_validators: Dict[OperandType, Callable] = {
            OperandType.STRING: self._validate_string,
            OperandType.NUMBER: self._validate_number,
            OperandType.DATE: self._validate_date,
            OperandType.BOOL: self._validate_boolean,
            OperandType.ENUM: self._validate_enum,
        }
        self._structured_data_validators: DefaultDict[OperandType, Callable] = defaultdict(
            lambda: self.validate_separated_field
        )
        self._structured_data_validators.update(
            {
                OperandType.TABLE: self.validate_table,
                OperandType.ARRAY: self.validate_array,
                OperandType.DICT: self.validate_dict,
            }
        )

    def validate(self, fields: List[BaseDataToValidate]) -> ValidationResultDTO:
        validation_result = ValidationResultDTO()

        for local_field in fields:
            field_validation_result = self.validate_field(local_field)
            if field_validation_result.errors:
                validation_result.detail.append(field_validation_result)
                validation_result.is_valid = False

        return validation_result

    def validate_field(self, field: BaseDataToValidate):
        validation_function = self._structured_data_validators[field.field_type]
        return validation_function(field)

    def perform_validation(self, field: BaseDataToValidate, issues: Issues) -> None:
        validation_function = self._structured_data_validators[field.field_type]
        field_issues = validation_function(field)
        issues.add_pre_check_issues(
            errors=[message.as_issue() for message in field_issues.errors],
            warnings=[message.as_issue() for message in field_issues.warnings],
        )

    def validate_separated_field(self, field: FieldDataToValidate) -> FieldValidationIssues:
        validation_issues = FieldValidationIssues(field.field_code, field.document_id)
        if not has_value(field.data.value):
            return validation_issues

        field_type_validator = self._base_data_validators.get(OperandType(field.field_type))
        if not field_type_validator:
            validation_issues.errors.append(Message(message=f"Unknown type {field.field_type}"))
            return validation_issues

        try:
            field_type_validator(field.data.value, field.meta)
        except InvalidType as e:
            validation_issues.errors.append(Message(message=e.msg))

        return validation_issues

    def validate_table(self, field: TableDataToValidate):
        validation_issues = FieldValidationIssues(field_code=field.field_code, document_id=field.document_id)

        for column_meta in field.meta.columns:  # noqa: WPS426
            column_cells = filter(
                lambda cell: cell.coordinates.column == column_meta.index,
                field.data.cells,
            )

            cell_type_validator = self._base_data_validators[OperandType(column_meta.item_type)]
            for local_cell in column_cells:
                if not has_value(local_cell.value):
                    continue
                error = self._validate_cell(cell_type_validator, local_cell.value, column_meta.meta)
                if error:
                    validation_issues.errors.append(
                        Message(
                            message=error,
                            column=local_cell.coordinates.column,
                            row=local_cell.coordinates.row,
                        )
                    )

        add_error_marker(field, validation_issues)

        return validation_issues

    def validate_array(self, field: ArrayDataToValidate):
        validation_issues = FieldValidationIssues(field_code=field.field_code, document_id=field.document_id)
        if not field.data.items and not field.is_required:
            return validation_issues

        try:
            self._validate_array(field.data.items, field.meta)
        except InvalidType as e:
            validation_issues.errors.append(Message(message=e.msg))
            return validation_issues

        for index, local_field in enumerate(field.data.items):
            issues = self.validate_field(local_field)
            validation_issues.errors.extend(
                [
                    Message(
                        message=error.message,
                        column=error.column,
                        row=error.row,
                        index=index,
                        kv_id=error.kv_id,
                    )
                    for error in issues.errors
                ]
            )

        add_error_marker(field, validation_issues)

        return validation_issues

    def validate_dict(self, field: DictDataToValidate):
        validation_issues = FieldValidationIssues(field_code=field.field_code, document_id=field.document_id)

        try:
            self._validate_dict(field.data.items)
        except InvalidType as e:
            validation_issues.errors.append(Message(message=e.msg))
            return validation_issues

        for index, item in enumerate(field.data.items):
            if has_value(item.data.value):
                item_type_validator = self._base_data_validators.get(OperandType(item.field_type))
                if not item_type_validator:
                    validation_issues.errors.append(
                        Message(
                            message=f"Unknown type of {DICT_ITEMS[index]}: {item.field_type}",
                            kv_id=DICT_ITEMS[index],
                        )
                    )
                error = self._validate_dict_item(item_type_validator, item.data.value, item.meta)
                if error:
                    validation_issues.errors.append(Message(message=error, kv_id=DICT_ITEMS[index]))

        return validation_issues

    @staticmethod
    def _validate_dict(items: Any):
        if len(items) != 2:
            raise InvalidType("Field is not a key/value pair")

        return items

    @staticmethod
    def _validate_dict_item(item_type_validator, item, item_meta):
        try:
            item_type_validator(item, item_meta)
        except InvalidType as e:
            return e.msg

    @staticmethod
    def _validate_cell(validator: Callable, value: Any, meta: Any) -> Union[None, str]:
        try:
            validator(value, meta)
        except InvalidType as e:
            return e.msg

    @staticmethod
    def _validate_array(field_value: Any, field_meta: ArrayFieldTypeMeta):
        if not isinstance(field_value, list):
            raise InvalidType("Field value is not an array")

        return field_value

    @staticmethod
    def _validate_string(field_value: Any, field_meta: StringFieldTypeMeta) -> str:
        if not isinstance(field_value, str):
            raise InvalidType("Field is not a string")

        return field_value

    @classmethod
    def _validate_number(cls, field_value: Any, field_meta: BasicFieldTypeMeta) -> float:
        try:
            field_value = float(field_value)  # type: ignore
        except (ValueError, TypeError):
            raise InvalidType("Field is not a number")
        if field_meta.allowed_values and field_value not in field_meta.allowed_values:
            raise InvalidType(f"Field value should be from {field_meta.allowed_values}")
        if field_meta.restricted_values and field_value in field_meta.restricted_values:
            raise InvalidType(f"Field value should not be from {field_meta.restricted_values}")
        if not (cls.NUMBER_LOWER_BOUNDARY < field_value < cls.NUMBER_UPPER_BOUNDARY):  # noqa: WPS508
            interval = (cls.NUMBER_LOWER_BOUNDARY, cls.NUMBER_UPPER_BOUNDARY)
            raise InvalidType(f"Value is out of supported range: {interval}")

        return field_value

    @classmethod
    def _validate_date(cls, field_value: Any, field_meta: Union[DateFieldTypeMeta, BasicFieldTypeMeta]) -> datetime:
        format_ = getattr(field_meta, "format", None)
        if format_ is None or isinstance(field_meta, BasicFieldTypeMeta):
            result = cls._validate_date_for_known_formats(field_value)
        else:
            result = cls._validate_date_format(field_value, format_)

        if not (cls.DATE_LOWER_BOUNDARY <= result.date() <= cls.DATE_UPPER_BOUNDARY):  # noqa: WPS508
            interval = (
                cls.DATE_LOWER_BOUNDARY.strftime(DATE_FORMATS[0]),
                cls.DATE_UPPER_BOUNDARY.strftime(DATE_FORMATS[0]),
            )
            raise InvalidType(f"Value is out of supported range: {interval}")
        return result

    @staticmethod
    def _validate_boolean(field_value: Any, field_meta: BasicFieldTypeMeta) -> bool:
        if not isinstance(field_value, bool):
            raise InvalidType("Field is not a bool")
        return field_value

    @staticmethod
    def _validate_enum(field_value: Any, field_meta: EnumFieldTypeMeta) -> Any:
        options = field_meta.options
        if field_value not in options:
            options_str = ", ".join(f"'{option}'" for option in options)
            raise InvalidType(f"Field value should be one of the following options: {options_str}")
        return field_value

    @staticmethod
    def _validate_date_for_known_formats(field_value: Any) -> datetime:
        for num, field_format in enumerate(DATE_FORMATS):
            try:
                result = datetime.strptime(field_value, field_format)  # type: ignore
                break
            except (ValueError, TypeError):
                if num == len(DATE_FORMATS) - 1:
                    raise InvalidType("Field is not a date or invalid date format")
        return result

    @staticmethod
    def _validate_date_format(field_value: Any, format: str) -> datetime:
        try:
            return datetime.strptime(field_value, format)  # type: ignore
        except (ValueError, TypeError):
            raise InvalidType("Field is not a date or invalid date format")
