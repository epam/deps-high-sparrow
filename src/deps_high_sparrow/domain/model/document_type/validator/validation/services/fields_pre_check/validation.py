import logging
from collections import defaultdict
from typing import Callable, DefaultDict, List

from ......validation_result import Issues
from ...dto.prepared_field import (
    ArrayDataToValidate,
    BaseDataToValidate,
    DictDataToValidate,
    FieldDataToValidate,
    TableDataToValidate,
)
from ...dto.validation import ValidationResultDTO
from ...entities.constants import DICT_ITEMS, OperandType, Severity
from ...interfaces import IValidationService
from ..utils import (
    FieldValidationIssues,
    Message,
    add_error_marker,
    all_table_cells_in_bounds,
    field_full_name,
    has_value,
)

logger = logging.getLogger(__name__)


class RequiredFieldsPreCheckService(IValidationService):
    FIELD_IS_REQUIRED_MSG = "Field is required"
    COLUMN_IS_REQUIRED_MSG = "Column is required"
    CELLS_OUT_OF_BOUNDS = "Some cells are outside of the defined columns"
    ITEM_IS_REQUIRED_MSG = ("Key is required", "Value is required")

    def __init__(self):
        self._field_types_pre_validators: DefaultDict[OperandType, Callable] = defaultdict(
            lambda: self.validate_separated_field
        )
        self._field_types_pre_validators[OperandType.TABLE] = self.validate_table
        self._field_types_pre_validators[OperandType.ARRAY] = self.validate_array
        self._field_types_pre_validators[OperandType.DICT] = self.validate_dict

    def validate(self, fields: List[BaseDataToValidate]) -> ValidationResultDTO:
        validation_result = ValidationResultDTO()

        if not fields:
            return validation_result

        for field in fields:
            field_validation_result = self.validate_field(field)
            if field_validation_result.errors:
                validation_result.detail.append(field_validation_result)
                validation_result.is_valid = False

        return validation_result

    def validate_field(self, field: BaseDataToValidate) -> FieldValidationIssues:
        validator = self._field_types_pre_validators[field.field_type]
        return validator(field)

    def perform_validation(self, field: BaseDataToValidate, issues: Issues) -> None:
        validator = self._field_types_pre_validators[field.field_type]
        field_issues = validator(field)
        issues.add_pre_check_issues(
            errors=[message.as_issue() for message in field_issues.errors],
            warnings=[message.as_issue() for message in field_issues.warnings],
        )

    def create_issues_for_empty_value(self, code: str, issues: Issues) -> None:
        field_issues = FieldValidationIssues(code, -1)
        field_issues.add(Severity.ERROR, Message(message=self.FIELD_IS_REQUIRED_MSG))
        issues.add_pre_check_issues(
            errors=[message.as_issue() for message in field_issues.errors],
            warnings=[message.as_issue() for message in field_issues.warnings],
        )

    def validate_separated_field(self, field: FieldDataToValidate) -> FieldValidationIssues:
        if (field.data is None or not has_value(field.data.value)) and field.is_required:
            logger.error(f"Field {field_full_name(field)} is required")
            return self._create_field_issues(field, self.FIELD_IS_REQUIRED_MSG)

        return FieldValidationIssues(field.field_code, field.document_id)

    def validate_table(self, field: TableDataToValidate) -> FieldValidationIssues:
        one_cell_has_value = any(has_value(cell.value) for cell in field.data.cells) if field.data else False
        if (field.data is None or not one_cell_has_value) and field.is_required:
            logger.error(f"Field {field_full_name(field)} is required")
            field.is_column_size_correct = False
            return self._create_field_issues(field=field, message=self.FIELD_IS_REQUIRED_MSG)

        if field.data is not None and field.data.cells:
            if not all_table_cells_in_bounds(table_data=field):
                logger.warning(f"Some cells of {field_full_name(field)} in non existing columns")
                field.is_column_size_correct = False
                return self._create_field_issues(field=field, message=self.CELLS_OUT_OF_BOUNDS)

            field_issues = self._validate_table_cells(field)
        else:
            field_issues = FieldValidationIssues(field_code=field.field_code, document_id=field.document_id)

        add_error_marker(field=field, validation_issues=field_issues)

        return field_issues

    def validate_array(self, field: ArrayDataToValidate) -> FieldValidationIssues:
        if not field.data.items and field.is_required:
            return self._create_field_issues(field, self.FIELD_IS_REQUIRED_MSG)

        validator = self._field_types_pre_validators[field.meta.item_type]
        field_issues = FieldValidationIssues(field.field_code, field.document_id)
        for index, item in enumerate(field.data.items):
            issues: FieldValidationIssues = validator(item)
            for error in issues.errors:
                field_issues.add(
                    Severity.ERROR,
                    Message(
                        message=error.message,
                        column=error.column,
                        row=error.row,
                        index=index,
                        kv_id=error.kv_id,
                    ),
                )

        add_error_marker(field, field_issues)

        return field_issues

    def validate_dict(self, field: DictDataToValidate) -> FieldValidationIssues:
        field_issues = FieldValidationIssues(field.field_code, field.document_id)
        if field.is_required:
            for index, item in enumerate(field.data.items):
                if not (has_value(item.data.value)):
                    field_issues.add(
                        Severity.ERROR,
                        Message(
                            message=self.ITEM_IS_REQUIRED_MSG[index],
                            kv_id=DICT_ITEMS[index],
                        ),
                    )
                    logger.error(f"{DICT_ITEMS[index].capitalize()} of field {field_full_name(field)} is required")

        return field_issues

    @staticmethod
    def _create_field_issues(field: BaseDataToValidate, message: str) -> FieldValidationIssues:
        field_issues = FieldValidationIssues(field.field_code, field.document_id)
        field_issues.add(Severity.ERROR, Message(message=message))
        return field_issues

    def _validate_table_cells(self, field: TableDataToValidate) -> FieldValidationIssues:
        field_issues = FieldValidationIssues(field.field_code, field.document_id)

        for cell in field.data.cells:  # noqa: WPS426
            column_meta = next(
                filter(
                    lambda column: column.index == cell.coordinates.column,
                    field.meta.columns,
                )
            )
            if not has_value(cell.value) and column_meta.is_required:
                field_issues.add(
                    Severity.ERROR,
                    Message(
                        message=self.COLUMN_IS_REQUIRED_MSG,
                        column=cell.coordinates.column,
                        row=cell.coordinates.row,
                    ),
                )
                logger.debug(
                    "Cell %s|%s for field %s is required",
                    cell.coordinates.row,
                    cell.coordinates.column,
                    field_full_name(field),
                )

        return field_issues
