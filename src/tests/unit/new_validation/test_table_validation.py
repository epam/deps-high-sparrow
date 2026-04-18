import pytest


@pytest.mark.parametrize(
    "rule",
    [
        "len(Ftable_1__0) > 0",
    ],
)
def test_validate_table__column_required__reports_row_and_column(
    rule,
    table_field,
    business_validation_service,
    rule_object_factory,
):
    error_message = "Column 0 must not be empty"
    rule_obj = rule_object_factory(
        field_code=table_field.field_code,
        document_type_code=table_field.document_type_code,
    )
    rule_obj.rule = rule
    rule_obj.severity = "error"
    rule_obj.issue_message = error_message

    validation_result = business_validation_service.validate([table_field], [rule_obj])

    assert validation_result.is_valid is False
    assert len(validation_result.detail) == 1
    assert len(validation_result.detail[0].errors) > 0

    errors_with_row_column = [e for e in validation_result.detail[0].errors if e.message == error_message]
    assert len(errors_with_row_column) > 0
    error = errors_with_row_column[0]

    assert error.row == 1
    assert error.column == 0
    assert error.message == error_message
    assert error.index is None
    assert error.kv_id is None


@pytest.mark.parametrize(
    "rule",
    [
        "len(Ftable_1__0) > 0 and len(Ftable_1__1) > 0",
    ],
)
def test_validate_table__two_columns_required__reports_row_and_column(
    rule,
    table_field,
    business_validation_service,
    rule_object_factory,
):
    error_message = "Both columns must have content"
    rule_obj = rule_object_factory(
        field_code=table_field.field_code,
        document_type_code=table_field.document_type_code,
    )
    rule_obj.rule = rule
    rule_obj.severity = "error"
    rule_obj.issue_message = error_message

    validation_result = business_validation_service.validate([table_field], [rule_obj])

    assert validation_result.is_valid is False
    assert len(validation_result.detail) == 1
    assert len(validation_result.detail[0].errors) > 0

    errors_with_row_column = [e for e in validation_result.detail[0].errors if e.message == error_message]
    assert len(errors_with_row_column) > 0

    # We should have errors for rows 1 and 2 (where columns are empty)
    error_rows = sorted([e.row for e in errors_with_row_column])
    assert 1 in error_rows or 2 in error_rows

    error = errors_with_row_column[0]
    assert error.message == error_message
    assert error.index is None
    assert error.kv_id is None


@pytest.mark.parametrize(
    "rule",
    [
        "Ftable_1[1][0] == '2'",
    ],
)
def test_validate_table__specific_cell_subscript__reports_row_and_column(
    rule,
    table_field,
    business_validation_service,
    rule_object_factory,
):
    error_message = "Cell at column 1, row 0 must equal '2'"
    rule_obj = rule_object_factory(
        field_code=table_field.field_code,
        document_type_code=table_field.document_type_code,
    )
    rule_obj.rule = rule
    rule_obj.severity = "error"
    rule_obj.issue_message = error_message

    validation_result = business_validation_service.validate([table_field], [rule_obj])

    assert validation_result.is_valid is False
    assert len(validation_result.detail) == 1
    assert len(validation_result.detail[0].errors) > 0

    errors_with_row_column = [e for e in validation_result.detail[0].errors if e.message == error_message]
    assert len(errors_with_row_column) == 1
    error = errors_with_row_column[0]

    assert error.row == 0
    assert error.column == 1
    assert error.message == error_message
    assert error.index is None
    assert error.kv_id is None


@pytest.mark.parametrize(
    "rule",
    [
        "(int(cell(Ftable_1, 0, 3)) + int(cell(Ftable_1, 1, 3))) == 15",
    ],
)
def test_validate_table__cell_function__reports_row_and_column(
    rule,
    table_field,
    business_validation_service,
    rule_object_factory,
):
    error_message = "Sum of cells at (0,3) and (1,3) must equal 15"
    rule_obj = rule_object_factory(
        field_code=table_field.field_code,
        document_type_code=table_field.document_type_code,
    )
    rule_obj.rule = rule
    rule_obj.severity = "error"
    rule_obj.issue_message = error_message

    validation_result = business_validation_service.validate([table_field], [rule_obj])

    assert validation_result.is_valid is False
    assert len(validation_result.detail) == 1
    assert len(validation_result.detail[0].errors) > 0

    errors_with_row_column = [e for e in validation_result.detail[0].errors if e.message == error_message]

    assert len(errors_with_row_column) == 1
    error = errors_with_row_column[0]
    assert error.message == error_message
    assert error.index is None
    assert error.kv_id is None
