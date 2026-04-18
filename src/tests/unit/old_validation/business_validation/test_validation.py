from unittest.mock import Mock

import pytest
from faker import Faker

from deps_high_sparrow.domain.model.document_type.validator.validation.services.utils import (
    Message,
)

VALIDATION_SERVICE_PATH = (
    "deps_better_validation.domain.services.business_validation.validation" ".BusinessRulesValidationService"
)
RULE_REPOSITORY_PATH = "deps_better_validation.infrastructure.repositories.rule.RuleRepository"

from deps_high_sparrow.domain.model.document_type.validator.validation.dto.field import (
    BasicFieldTypeMeta,
    ColumnTypeMeta,
    TableFieldTypeMeta,
)
from deps_high_sparrow.domain.model.document_type.validator.validation.dto.prepared_field import (
    Cell,
    Coordinates,
    TableData,
    TableDataToValidate,
)
from deps_high_sparrow.domain.model.document_type.validator.validation.entities.constants import (
    OperandType,
)

fake = Faker()


@pytest.fixture(params=((None, None), (None, ""), ("", None), ("", "")))
def invalid_data_set_for_depended_rule(request):
    return request.param


@pytest.fixture(params=(("test", "test"), ("test", 0), (0, "test")))
def valid_data_set_for_depended_rule(request, invalid_data_set_for_depended_rule):
    depended_item, item_for_check = request.param
    return (
        depended_item if depended_item else invalid_data_set_for_depended_rule[0],
        item_for_check if item_for_check else invalid_data_set_for_depended_rule[1],
    )


@pytest.fixture
def prepared_table_field(document_id):
    return TableDataToValidate(
        document_id=document_id,
        field_code="field_code3",
        document_type_code="document_type3",
        field_type=OperandType.TABLE,
        is_required=True,
        meta=TableFieldTypeMeta(
            columns=[
                ColumnTypeMeta(
                    index=0,
                    is_required=True,
                    item_type=OperandType.NUMBER,
                    meta=BasicFieldTypeMeta(),
                ),
                ColumnTypeMeta(
                    index=1,
                    is_required=False,
                    item_type=OperandType.DATE,
                    meta=BasicFieldTypeMeta(),
                ),
                ColumnTypeMeta(
                    index=0,
                    is_required=True,
                    item_type=OperandType.NUMBER,
                    meta=BasicFieldTypeMeta(),
                ),
                ColumnTypeMeta(
                    index=1,
                    is_required=False,
                    item_type=OperandType.DATE,
                    meta=BasicFieldTypeMeta(),
                ),
            ]
        ),
        data=TableData(
            cells=[
                Cell(value="1", coordinates=Coordinates(column=0, row=0)),
                Cell(value="01-01-2000", coordinates=Coordinates(column=1, row=0)),
                Cell(value="1", coordinates=Coordinates(column=2, row=0)),
                Cell(value="01-01-2000", coordinates=Coordinates(column=3, row=0)),
            ]
        ),
    )


def test_validate__empty_fields(business_validation_service):
    validation_result = business_validation_service.validate([], [])
    assert validation_result.is_valid is True
    assert validation_result.detail == []


def test_validate__is_valid(
    number_casted_field,
    rule_number,
    number_filed_name,
    business_validation_service,
):
    rule_number.rule = f"{number_filed_name} == 1"
    rule_number.severity = "warning"

    validation_result = business_validation_service.validate([number_casted_field], [rule_number])
    assert validation_result.is_valid
    assert validation_result.detail == []


def test_validate__is_not_valid(
    number_casted_field,
    rule_number,
    number_filed_name,
    business_validation_service,
):
    rule_number.rule = f"{number_filed_name} == 55"
    rule_number.severity = "error"

    validation_result = business_validation_service.validate([number_casted_field], [rule_number])
    assert validation_result.is_valid is False
    assert validation_result.detail[0].errors


def test_validate__warning_but_valid(
    number_casted_field,
    rule_number,
    number_filed_name,
    business_validation_service,
):
    rule_number.rule = f"{number_filed_name} == 55"
    rule_number.severity = "warning"

    validation_result = business_validation_service.validate([number_casted_field], [rule_number])
    assert validation_result.is_valid is True
    assert validation_result.detail[0].warnings


def test_validate__2_rules_is_not_valid(
    number_casted_field,
    two_rule_number,
    number_filed_name,
    business_validation_service,
):
    rule_1, rule_2 = two_rule_number
    rule_1.rule = f"{number_filed_name} == 55"
    rule_1.severity = "error"
    rule_2.rule = f"{number_filed_name} == 55"
    rule_2.severity = "warning"

    validation_result = business_validation_service.validate([number_casted_field], two_rule_number)

    assert validation_result.is_valid is False
    assert validation_result.detail[0].errors
    assert validation_result.detail[0].warnings


def test_validate__parser_raises_exception__validation_result_is_not_empty(
    string_casted_field, rule_string, business_validation_service
):
    rule_string.rule = "UNPARSABLE"
    rule_string.severity = "error"

    validation_result = business_validation_service.validate([string_casted_field], [rule_string])
    assert validation_result.is_valid is False
    assert validation_result.detail[0].errors


def test_validate_table__is_valid(
    table_casted_field,
    rule_table,
    table_filed_name,
    business_validation_service,
):
    rule_table.rule = f"{table_filed_name}__0 == 1"
    rule_table.severity = "error"

    validation_result = business_validation_service.validate([table_casted_field], [rule_table])
    assert validation_result.is_valid is True
    assert validation_result.detail == []


def test_validate_table__is_failed(
    table_casted_field,
    rule_table,
    table_filed_name,
    table_issues,
    business_validation_service,
):
    rule_table.rule = f"{table_filed_name}__0 != 1"
    rule_table.severity = "error"

    validation_result = business_validation_service.validate([table_casted_field], [rule_table])
    assert validation_result.is_valid is False
    assert validation_result.detail[0].errors == [table_issues[0], table_issues[-1]]


def test_validate_table__two_columns__is_valid(
    table_casted_field,
    rule_table,
    table_filed_name,
    business_validation_service,
):
    rule_table.rule = f"{table_filed_name}__0 < {table_filed_name}__1"
    rule_table.severity = "error"

    validation_result = business_validation_service.validate([table_casted_field], [rule_table])
    assert validation_result.is_valid is True
    assert validation_result.detail == []


def test_validate_table__two_columns__missed_optional_cell__is_valid(
    table_casted_field,
    rule_table,
    table_filed_name,
    business_validation_service,
    empty_value,
):
    table_casted_field.data.cells[-1].value = empty_value
    rule_table.rule = f"{table_filed_name}__0 < {table_filed_name}__1"
    rule_table.severity = "error"

    validation_result = business_validation_service.validate([table_casted_field], [rule_table])
    assert validation_result.is_valid is True
    assert validation_result.detail == []


def test_validate_table__two_columns__is_failed(
    table_casted_field,
    rule_table,
    table_filed_name,
    table_issues,
    business_validation_service,
):
    rule_table.rule = f"{table_filed_name}__0 > {table_filed_name}__1"
    rule_table.severity = "error"

    validation_result = business_validation_service.validate([table_casted_field], [rule_table])

    assert validation_result.is_valid is False
    assert validation_result.detail[0].errors == table_issues


def test_add_validation_markers__table_field(
    prepared_table_field, list_of_severity_message_tuples, business_validation_service
):
    business_validation_service._add_validation_markers(prepared_table_field, list_of_severity_message_tuples)
    messages = [message for _, message in list_of_severity_message_tuples]
    assert Message(message="Table contains errors") in messages
    assert Message(message="Table contains warnings") in messages


def test_add_validation_markers__array_field(
    prepared_default_array_field,
    list_of_severity_message_tuples,
    business_validation_service,
):
    business_validation_service._add_validation_markers(prepared_default_array_field, list_of_severity_message_tuples)
    messages = [message for _, message in list_of_severity_message_tuples]
    assert Message(message="Array contains errors") in messages
    assert Message(message="Array contains warnings") in messages


def test_add_validation_markers__array_of_tables_field(
    prepared_array_of_tables_field,
    list_of_severity_message_tuples,
    business_validation_service,
):
    business_validation_service._add_validation_markers(prepared_array_of_tables_field, list_of_severity_message_tuples)
    messages = [message for _, message in list_of_severity_message_tuples]
    assert Message(message="Array contains errors") in messages
    assert Message(message="Array contains warnings") in messages


def test_add_validation_markers__empty_errors_and_warnings(
    prepared_table_field, list_of_severity_message_tuples, business_validation_service
):
    list_of_severity_message_tuples = []
    business_validation_service._add_validation_markers(prepared_table_field, list_of_severity_message_tuples)
    messages = [message for _, message in list_of_severity_message_tuples]
    assert messages == []


def test_validate_table__depended_rule__is_failed(
    table_casted_field,
    rule_table,
    table_filed_name,
    table_issues,
    business_validation_service,
    invalid_data_set_for_depended_rule,
):
    rule_table.rule = f"check_dependency({table_filed_name}__0, {table_filed_name}__1)"
    table_casted_field.data.cells[0].value = invalid_data_set_for_depended_rule[0]
    table_casted_field.data.cells[1].value = invalid_data_set_for_depended_rule[1]
    rule_table.severity = "error"

    validation_result = business_validation_service.validate([table_casted_field], [rule_table])

    assert validation_result.is_valid is False
    assert validation_result.detail[0].errors == table_issues


def test_validate_table__depended_rule__is_valid(
    table_casted_field,
    rule_table,
    table_filed_name,
    business_validation_service,
    valid_data_set_for_depended_rule,
):
    table_casted_field.data.cells[0].value = valid_data_set_for_depended_rule[0]
    table_casted_field.data.cells[1].value = valid_data_set_for_depended_rule[1]
    rule_table.rule = f"check_dependency({table_filed_name}__0, {table_filed_name}__1)"
    rule_table.meta.check_optional_fields = True
    rule_table.severity = "error"

    validation_result = business_validation_service.validate([table_casted_field], [rule_table])

    assert validation_result.is_valid is True
    assert validation_result.detail == []


def test_validate_table__depended_rule__three_depended_columns__is_valid(
    table_casted_field,
    rule_table,
    table_filed_name,
    business_validation_service,
):
    rule_table.rule = (
        f"check_dependency({table_filed_name}__0, {table_filed_name}__1, {table_filed_name}__2, {table_filed_name}__3)"
    )
    rule_table.meta.check_optional_fields = True
    rule_table.severity = "error"

    validation_result = business_validation_service.validate([table_casted_field], [rule_table])

    assert validation_result.is_valid is True
    assert validation_result.detail == []


def test_validate_dict__is_valid(dict_casted_field, rule_dict, dict_filed_name, business_validation_service):
    rule_dict.rule = f"{dict_filed_name}__0 == 'val'"
    rule_dict.severity = "error"

    validation_result = business_validation_service.validate([dict_casted_field], [rule_dict])
    assert validation_result.is_valid
    assert validation_result.detail == []

    rule_dict.rule = f"{dict_filed_name}[0] == 'val'"
    rule_dict.severity = "error"

    validation_result = business_validation_service.validate([dict_casted_field], [rule_dict])
    assert validation_result.is_valid
    assert validation_result.detail == []


def test_validate_dict__warning_is_valid(dict_casted_field, rule_dict, dict_filed_name, business_validation_service):
    rule_dict.rule = f"{dict_filed_name}__0 != 'val'"
    rule_dict.severity = "warning"

    validation_result = business_validation_service.validate([dict_casted_field], [rule_dict])
    assert validation_result.is_valid
    assert validation_result.detail[0].warnings

    rule_dict.rule = f"{dict_filed_name}[0] != 'val'"
    rule_dict.severity = "warning"

    validation_result = business_validation_service.validate([dict_casted_field], [rule_dict])
    assert validation_result.is_valid
    assert validation_result.detail[0].warnings


def test_validate_dict__is_not_valid(dict_casted_field, rule_dict, dict_filed_name, business_validation_service):
    rule_dict.rule = f"{dict_filed_name}__0 != 'val'"
    rule_dict.severity = "error"

    validation_result = business_validation_service.validate([dict_casted_field], [rule_dict])
    assert not validation_result.is_valid
    assert validation_result.detail[0].errors

    rule_dict.rule = f"{dict_filed_name}[0] != 'val'"
    rule_dict.severity = "error"

    validation_result = business_validation_service.validate([dict_casted_field], [rule_dict])
    assert not validation_result.is_valid
    assert validation_result.detail[0].errors


def test_validate_dict__rule_error__not_raised(dict_casted_field, rule_dict, business_validation_service):
    rule_dict.rule = f"wrong_field_name__0 == 'val'"
    rule_dict.severity = "error"

    validation_result = business_validation_service.validate([dict_casted_field], [rule_dict])
    assert not validation_result.is_valid
    assert validation_result.detail[0].errors


def test_validate_table__column_level_rule__error_per_row(
    table_casted_field_multi_row,
    rule_table,
    business_validation_service,
):
    column_var = f"{table_casted_field_multi_row.document_type_code}__{table_casted_field_multi_row.field_code}__0"
    rule_table.rule = f"{column_var} == 'impossible_value'"
    rule_table.severity = "error"

    validation_result = business_validation_service.validate([table_casted_field_multi_row], [rule_table])

    assert validation_result.is_valid is False
    errors_with_position = [error for error in validation_result.detail[0].errors if error.row is not None]
    assert len(errors_with_position) == 2
    assert {error.row for error in errors_with_position} == {0, 1}
    assert all(error.column == 0 for error in errors_with_position)


def test_validate_table__subscript_rule__single_error(
    table_casted_field_multi_row,
    rule_table,
    business_validation_service,
):
    rule_table.rule = "Ffield_code3[0][0] == 'impossible_value'"
    rule_table.severity = "error"

    variables = {
        "Ffield_code3": {
            0: {0: 1, 1: 2},
            1: {0: "date1", 1: "other"},
        }
    }

    validation_result = business_validation_service._validate_table(
        table_casted_field_multi_row,
        [rule_table],
        variables,
        set(),
    )

    errors_with_position = [(sev, msg) for sev, msg in validation_result if msg.row is not None]
    assert len(errors_with_position) == 1
    assert errors_with_position[0][1].column == 0
    assert errors_with_position[0][1].row == 0


def test_validate_table__empty_table__no_errors(
    table_casted_field,
    rule_table,
    business_validation_service,
):
    table_casted_field.data.cells = []
    column_var = f"{table_casted_field.document_type_code}__{table_casted_field.field_code}__0"
    rule_table.rule = f"{column_var} == 'test'"
    rule_table.severity = "error"

    validation_result = business_validation_service.validate([table_casted_field], [rule_table])

    assert validation_result.detail == []
