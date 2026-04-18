import logging
import re
from collections import defaultdict
from typing import Any, Callable, DefaultDict, Dict, List, Optional, Set, Tuple, Union

from ......validation_result import Issues
from ...dto.prepared_field import (
    ArrayDataToValidate,
    BaseDataToValidate,
    Cell,
    DictDataToValidate,
    FieldDataToValidate,
    TableDataToValidate,
)
from ...dto.validation import ValidationResultDTO
from ...entities.constants import DICT_ITEMS, KeyValueId, OperandType, Severity
from ...entities.rule import RuleEntity
from ...exceptions import CompareWithOptionalField
from ...interfaces import IValidationService
from ..constants import NAME_SEPARATOR
from ..utils import (
    FieldValidationIssues,
    Message,
    build_colum_full_name,
    build_dict_item_full_name,
    build_modern_field_name,
    field_full_name,
    fields_values_hash_table,
    has_value,
    is_errors,
    is_validation_issues,
    sanitize_rule,
)
from .parser import ValidationRuleParser
from .rule_position_extractor import RulePositionExtractor

logger = logging.getLogger(__name__)


class BusinessRulesValidationService(IValidationService):
    MARKER_MSG_TEMPLATE = "{0} contains {1}s"
    SYSTEM_ERROR_MESSAGE = "System Error: Failed to parse validation rule"

    def __init__(self):
        self._position_extractor = RulePositionExtractor()
        self._validation_data_mappers: DefaultDict[OperandType, Callable] = defaultdict(
            lambda: self._validate_separated_field
        )
        self._validation_data_mappers.update(
            {
                OperandType.ARRAY: self._validate_array,
                OperandType.TABLE: self._validate_table,
                OperandType.DICT: self._validate_dict,
            }
        )

    def validate(
        self,
        fields: List[BaseDataToValidate],
        rules: list[RuleEntity],
        context_fields: Optional[List[BaseDataToValidate]] = None,
    ) -> ValidationResultDTO:
        context_fields = context_fields if context_fields else []
        validation_result = ValidationResultDTO()

        grouped_fields_rules = self._group_fields_rules(rules)
        fields_validation_issues = self._validate_fields(fields, grouped_fields_rules, context_fields)

        for issues in fields_validation_issues:
            if is_validation_issues(issues):
                validation_result.detail.append(issues)

            if validation_result.is_valid and is_errors(issues):
                validation_result.is_valid = False

        return validation_result

    def validate_field(self, field: BaseDataToValidate, rules: list[RuleEntity]) -> FieldValidationIssues:
        fields = [field]
        grouped_fields_rules = self._group_fields_rules(rules)
        variables = fields_values_hash_table(fields)
        validation_issues = FieldValidationIssues(field_code=field.field_code, document_id=field.document_id)
        for field in fields:
            rules = grouped_fields_rules.get(field_full_name(field))
            if not rules:
                continue

            validation_function = self._validation_data_mappers[field.field_type]
            issues = validation_function(field, rules, variables, set())  # type: ignore

            if issues:
                for severity, message in issues:
                    validation_issues.add(severity=severity, message=message)

        return validation_issues

    def perform_validation(self, field: BaseDataToValidate, rules: list[RuleEntity], issues: Issues) -> None:
        fields = [field]
        grouped_fields_rules = self._group_fields_rules(rules)
        variables = fields_values_hash_table(fields)
        validation_issues = FieldValidationIssues(field_code=field.field_code, document_id=field.document_id)
        for field in fields:
            rules = grouped_fields_rules.get(field_full_name(field))
            if not rules:
                continue

            validation_function = self._validation_data_mappers[field.field_type]
            field_issues = validation_function(field, rules, variables, set())  # type: ignore

            if field_issues:
                for severity, message in field_issues:
                    validation_issues.add(severity=severity, message=message)

        issues.add_rules_check_issues(
            errors=[error_message.as_issue() for error_message in validation_issues.errors],
            warnings=[warning_message.as_issue() for warning_message in validation_issues.warnings],
        )

    @staticmethod
    def _group_fields_rules(rules: List[RuleEntity]) -> Dict[str, List[RuleEntity]]:
        grouped_fields_rules: Dict[str, List[RuleEntity]] = {}
        for rule in rules:
            full_name = field_full_name(rule)
            sanitized_rule = sanitize_rule(rule)
            if full_name in grouped_fields_rules:
                grouped_fields_rules[full_name].append(sanitized_rule)
                continue
            grouped_fields_rules[full_name] = [sanitized_rule]
        return grouped_fields_rules

    def _validate_fields(
        self,
        fields: List[BaseDataToValidate],
        grouped_rules: Dict[str, List[RuleEntity]],
        context_fields: List[BaseDataToValidate],
    ) -> List[FieldValidationIssues]:
        variables = fields_values_hash_table(fields + context_fields)
        for field in fields + context_fields:
            if isinstance(field, ArrayDataToValidate):
                variables.update(fields_values_hash_table(field.data.items))  # type: ignore
            if isinstance(field, DictDataToValidate):
                variables.update(fields_values_hash_table(field.data.items))  # type: ignore

        fields_validation_issues = []
        for field in fields:
            rules = grouped_rules.get(field_full_name(field))
            if not rules:
                continue

            validation_function = self._validation_data_mappers[field.field_type]
            issues = validation_function(field, rules, variables, set())  # type: ignore

            if issues:
                validation_issues = FieldValidationIssues(field_code=field.field_code, document_id=field.document_id)
                for severity, message in issues:
                    validation_issues.add(severity=severity, message=message)
                fields_validation_issues.append(validation_issues)

        return fields_validation_issues

    def _validate_array(
        self,
        field: ArrayDataToValidate,
        rules: List[RuleEntity],
        variables: Dict[str, Any],
        optional_fields: Set[str],
    ) -> List[Tuple[Severity, Message]]:
        rules_for_each = [rule for rule in rules if rule.meta.for_each]
        rules_for_any = [rule for rule in rules if rule.meta.for_any]
        rules_for_whole_list = [rule for rule in rules if not rule.meta.for_each and not rule.meta.for_any]

        validation_function = self._validation_data_mappers[field.meta.item_type]

        items_validation_issues = self._validate_each_array_item(
            field.data.items,
            rules_for_each,
            validation_function,
            variables,
            optional_fields,
        )
        items_validation_issues.extend(
            self._validate_any_array_item(
                field.data.items,
                rules_for_any,
                validation_function,
                variables,
                optional_fields,
            )
        )

        self._add_validation_markers(field, items_validation_issues)

        array_validation_issues = self._validate_array_level_rules(
            field, rules_for_whole_list, variables, optional_fields
        )
        items_validation_issues.extend(array_validation_issues)

        return items_validation_issues

    def _validate_each_array_item(
        self,
        items: Union[
            List[FieldDataToValidate],
            List[TableDataToValidate],
            List[DictDataToValidate],
        ],
        rules_for_each: List[RuleEntity],
        validation_function: Callable,
        variables: Dict[str, Any],
        optional_fields: Set[str],
    ) -> List[Tuple[Severity, Message]]:
        issues_for_each = []
        for index, item_field in enumerate(items):
            local_variables = {**variables, **fields_values_hash_table([item_field])}
            item_issues = validation_function(item_field, rules_for_each, local_variables, optional_fields)
            issues_for_each.extend(self._build_array_issues(item_issues, index))

        return issues_for_each

    def _validate_any_array_item(
        self,
        items: Union[
            List[FieldDataToValidate],
            List[TableDataToValidate],
            List[DictDataToValidate],
        ],
        rules_for_any: List[RuleEntity],
        validation_function: Callable,
        variables: Dict[str, Any],
        optional_fields: Set[str],
    ) -> List[Tuple[Severity, Message]]:
        issues_for_any = []
        for rule in rules_for_any:
            any_issue_counter = 0
            rule_issues = []

            for index, item_field in enumerate(items):
                local_variables = {**variables, **fields_values_hash_table([item_field])}
                item_issues = validation_function(item_field, [rule], local_variables, optional_fields)
                if item_issues:
                    rule_issues.extend(self._build_array_issues(item_issues, index))
                    any_issue_counter += 1

            if any_issue_counter == len(items):
                issues_for_any.extend(rule_issues)

        return issues_for_any

    @staticmethod
    def _build_array_issues(issues: List[Tuple[Severity, Message]], index: int) -> List[Tuple[Severity, Message]]:
        return [
            (
                severity,
                Message(
                    message=message.message,
                    column=message.column,
                    row=message.row,
                    index=index,
                    kv_id=message.kv_id,
                ),
            )
            for severity, message in issues
        ]

    def _validate_array_level_rules(
        self,
        field: ArrayDataToValidate,
        rules: List[RuleEntity],
        variables: Dict[str, Any],
        optional_fields: Set[str],
    ) -> List[Tuple[Severity, Message]]:
        validation_issues = []

        for rule in rules:
            optional_fields_for_ignoring = optional_fields if rule.meta.check_optional_fields else None
            parser = ValidationRuleParser(variables=variables, optional_fields=optional_fields_for_ignoring)
            severity, message = self._validate_data(field, rule, parser)

            if message:
                index, kv_id = self._position_extractor.get_array_position(rule)
                validation_issues.append(
                    (severity, Message(message=message, index=index, kv_id=KeyValueId(kv_id) if kv_id else None))
                )

        return validation_issues

    def _validate_separated_field(
        self,
        field: BaseDataToValidate,
        rules: List[RuleEntity],
        variables: Dict[str, Any],
        optional_fields: Set[str],
    ) -> List[Tuple[Severity, Message]]:
        validation_issues = []

        for rule in rules:
            optional_fields_for_ignoring = optional_fields if rule.meta.check_optional_fields else None

            parser = ValidationRuleParser(variables=variables, optional_fields=optional_fields_for_ignoring)

            severity, message = self._validate_data(field, rule, parser)
            if message:
                validation_issues.append((severity, Message(message=message)))

        return validation_issues

    def _validate_table(
        self,
        field: TableDataToValidate,
        rules: List[RuleEntity],
        variables: Dict[str, Any],
        optional_fields: Set[str],
    ) -> List[Tuple[Severity, Message]]:
        rules_for_rows = []
        rules_for_whole_table = []
        for rule in rules:
            if self._position_extractor.has_explicit_cell_subscript(rule):
                rules_for_whole_table.append(rule)
            elif self._uses_column_level_variables(rule, field):
                rules_for_rows.append(rule)
            else:
                rules_for_whole_table.append(rule)

        validation_issues = self._validate_table_level_rules(field, rules_for_whole_table, variables, optional_fields)
        validation_issues.extend(self._validate_row_level_rules(field, rules_for_rows, variables, optional_fields))

        self._add_validation_markers(field, validation_issues)

        return validation_issues

    def _validate_table_level_rules(
        self,
        field: TableDataToValidate,
        rules: List[RuleEntity],
        variables: Dict[str, Any],
        optional_fields: Set[str],
    ) -> List[Tuple[Severity, Message]]:
        validation_issues = []

        for rule in rules:
            optional_fields_for_ignoring = optional_fields if rule.meta.check_optional_fields else None
            parser = ValidationRuleParser(
                variables=variables,
                optional_fields=optional_fields_for_ignoring,
            )
            severity, message = self._validate_data(field, rule, parser)
            if message:
                column, row = self._position_extractor.get_cell_position(rule)
                validation_issues.append((severity, Message(message=message, column=column, row=row)))

        return validation_issues

    def _validate_row_level_rules(
        self,
        field: TableDataToValidate,
        rules: List[RuleEntity],
        variables: Dict[str, Any],
        optional_fields: Set[str],
    ) -> List[Tuple[Severity, Message]]:
        validation_issues = []

        indexes_row = {cell.coordinates.row for cell in field.data.cells}
        for row_index in indexes_row:
            row = [cell for cell in field.data.cells if cell.coordinates.row == row_index]
            local_variables = {**self._get_table_row_values(field, row), **variables}
            local_optional_fields = {
                *self._get_table_row_optional_fields(field, row),
                *optional_fields,
            }
            for rule in rules:
                optional_fields_for_ignoring = local_optional_fields if rule.meta.check_optional_fields else None
                parser = ValidationRuleParser(
                    variables=local_variables,
                    optional_fields=optional_fields_for_ignoring,
                )
                severity, message = self._validate_data(field, rule, parser)
                if message:
                    for column in self._get_used_columns(parser):
                        validation_issues.append(  # noqa: WPS220
                            (
                                severity,
                                Message(message=message, column=column, row=row_index),
                            )
                        )
                del parser.used_variables

        return validation_issues

    @staticmethod
    def _get_table_row_values(field: TableDataToValidate, row: List[Cell]) -> Dict[str, Any]:
        values = {}
        modern_field_name = build_modern_field_name(field.field_code)

        for cell in row:
            legacy_key = build_colum_full_name(field, cell.coordinates.column)
            modern_key = f"{modern_field_name}__{cell.coordinates.column}"

            values[legacy_key] = cell.value
            values[modern_key] = cell.value

        return values

    @staticmethod
    def _get_table_row_optional_fields(field: TableDataToValidate, cells: List[Cell]) -> Set[str]:
        optional_values = set()
        modern_field_name = build_modern_field_name(field.field_code)

        for column in field.meta.columns:  # noqa: WPS426
            for local_cell in filter(lambda cell: cell.coordinates.column == column.index, cells):  # noqa: WPS426
                if not has_value(local_cell.value) and not column.is_required:
                    legacy_key = build_colum_full_name(field, column.index)
                    modern_key = f"{modern_field_name}__{column.index}"

                    optional_values.add(legacy_key)
                    optional_values.add(modern_key)
        return optional_values

    @staticmethod
    def _uses_column_level_variables(rule: RuleEntity, field: TableDataToValidate) -> bool:
        modern_field_name = build_modern_field_name(field.field_code)

        for column in field.meta.columns:
            legacy_column_name = re.escape(build_colum_full_name(field, column.index))
            modern_column_name = re.escape(f"{modern_field_name}__{column.index}")

            if re.search(rf"\b{legacy_column_name}\b", rule.rule):
                return True
            if re.search(rf"\b{modern_column_name}\b", rule.rule):
                return True

        return False

    @staticmethod
    def _validate_data(
        field: BaseDataToValidate,
        rule: RuleEntity,
        parser: ValidationRuleParser,
    ) -> Union[Tuple[Severity, str], Tuple[None, None]]:
        severity = Severity(rule.severity) if isinstance(rule.severity, str) else rule.severity

        logger.info(f"Check '{rule.name}' for '{field.field_code}' using rule '{rule.rule}'...")

        try:
            if not parser.parse(rule.rule):
                logger.info(f"Check is failed for {field.field_code}")
                return severity, rule.issue_message
        except CompareWithOptionalField:
            # If there is an optional field and user does not provide it, than
            # there is no chance to compare None to another field.
            # Can add any logic to handle it here.
            if rule.meta.need_warning_even_if_optional:
                return Severity.WARNING, rule.issue_message

        except Exception as exception:
            logger.error(f"Unexpected error: '{exception}' for '{field.field_code}'!")
            return severity, BusinessRulesValidationService.SYSTEM_ERROR_MESSAGE
        return None, None

    @staticmethod
    def _get_used_columns(parser) -> set[Optional[int]]:
        columns = set()
        for variable in parser.used_variables:
            try:
                columns.add(int(variable.split(NAME_SEPARATOR)[-1]))
            except TypeError:
                pass
            except ValueError:
                columns.add(None)
        return columns

    def _add_validation_markers(
        self,
        field: BaseDataToValidate,
        validation_issues: List[Tuple[Severity, Message]],
    ) -> None:
        markers_to_add = [severity for severity, _ in validation_issues]

        for marker in Severity:
            if marker in markers_to_add:
                validation_issues.append(
                    (
                        marker,
                        Message(
                            message=self.MARKER_MSG_TEMPLATE.format(field.field_type.value.capitalize(), marker.value)
                        ),
                    )
                )

    def _validate_dict(
        self,
        field: DictDataToValidate,
        rules: List[RuleEntity],
        variables: Dict[str, Any],
        optional_fields: Set[str],
    ) -> List[Tuple[Severity, Message]]:
        validation_issues = []

        local_optional_fields = {*self._get_dict_optional_fields(field), *optional_fields}
        dict_variables = {
            **fields_values_hash_table([field.data.items[0]]),
            **fields_values_hash_table([field.data.items[1]]),
            **variables,
        }

        for rule in rules:
            optional_fields_for_ignoring = local_optional_fields if rule.meta.check_optional_fields else None
            parser = ValidationRuleParser(variables=dict_variables, optional_fields=optional_fields_for_ignoring)
            severity, message = self._validate_data(field, rule, parser)

            legacy_field_name = field_full_name(field)
            modern_field_name = build_modern_field_name(field.field_code)
            index = self._position_extractor.get_dict_item_index(
                parser.used_variables, field, rule, legacy_field_name, modern_field_name
            )
            if message:
                validation_issues.append((severity, Message(message=message, kv_id=DICT_ITEMS[index])))
            del parser.used_variables

        return validation_issues

    @staticmethod
    def _get_dict_optional_fields(field: DictDataToValidate) -> Set[str]:
        optional_fields = set()
        if not field.is_required:
            for index, item in enumerate(field.data.items):
                if not has_value(item.data.value):
                    optional_fields.add(build_dict_item_full_name(field, index))
        return optional_fields
