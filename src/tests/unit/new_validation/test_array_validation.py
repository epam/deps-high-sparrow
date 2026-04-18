import pytest

from deps_high_sparrow.domain.model.document_type.validator.validation.entities.constants import (
    KeyValueId,
)


@pytest.mark.parametrize(
    "rule",
    [
        "Farray_field[1] > 100",
    ],
)
def test_validate_array__whole_array_rule_with_index__reports_index(
    rule,
    array_field_with_multiple_items,
    rule_object_factory,
    business_validation_service,
):
    error_message = "Value at index 1 wrong"
    rule_for_array = rule_object_factory(
        array_field_with_multiple_items.field_code, array_field_with_multiple_items.document_type_code
    )
    rule_for_array.rule = rule
    rule_for_array.severity = "error"
    rule_for_array.issue_message = error_message

    validation_result = business_validation_service.validate([array_field_with_multiple_items], [rule_for_array])

    assert validation_result.is_valid is False
    assert len(validation_result.detail) == 1
    assert len(validation_result.detail[0].errors) > 0

    errors_with_index = [e for e in validation_result.detail[0].errors if e.index is not None]
    assert len(errors_with_index) == 1
    error = errors_with_index[0]

    assert error.message == error_message
    assert error.index == 1
    assert error.kv_id is None
    assert error.column is None
    assert error.row is None


@pytest.mark.parametrize(
    "rule",
    [
        "Fitem_of__array_field != 20",
    ],
)
def test_validate_array__each_item_rule__reports_index(
    rule,
    array_field_with_multiple_items,
    rule_object_factory,
    business_validation_service,
):
    error_message = "Value at index 1 wrong"
    rule_for_array = rule_object_factory(
        array_field_with_multiple_items.field_code, array_field_with_multiple_items.document_type_code
    )
    rule_for_array.rule = rule
    rule_for_array.severity = "error"
    rule_for_array.issue_message = error_message
    rule_for_array.meta.for_each = True

    validation_result = business_validation_service.validate([array_field_with_multiple_items], [rule_for_array])

    assert validation_result.is_valid is False
    assert len(validation_result.detail) == 1
    assert len(validation_result.detail[0].errors) > 0

    errors_with_index = [e for e in validation_result.detail[0].errors if e.index is not None]
    assert len(errors_with_index) == 1
    error = errors_with_index[0]

    assert error.index == 1
    assert error.message == error_message
    assert error.kv_id is None
    assert error.column is None
    assert error.row is None


@pytest.mark.parametrize(
    "rule",
    [
        "len(Farray_field) > 10",
    ],
)
def test_validate_array__whole_array_rule_no_index__no_index_in_error(
    rule,
    array_field_with_multiple_items,
    rule_object_factory,
    business_validation_service,
):
    error_message = "Array should have more than 10 items"
    rule_for_array = rule_object_factory(
        array_field_with_multiple_items.field_code, array_field_with_multiple_items.document_type_code
    )
    rule_for_array.rule = rule
    rule_for_array.severity = "error"
    rule_for_array.issue_message = error_message

    validation_result = business_validation_service.validate([array_field_with_multiple_items], [rule_for_array])
    assert validation_result.is_valid is False
    assert len(validation_result.detail) == 1
    assert len(validation_result.detail[0].errors) > 0

    errors_with_message = [e for e in validation_result.detail[0].errors if "Array contains" not in e.message]
    assert len(errors_with_message) > 0
    error = errors_with_message[0]

    assert error.index is None
    assert error.kv_id is None
    assert error.column is None
    assert error.row is None


@pytest.mark.parametrize(
    "rule",
    [
        "Farray_dicts[1][0] == 'expected_key'",
    ],
)
def test_validate_array_of_dicts__key_validation__reports_index_and_kv_id_key(
    rule,
    rule_object_factory,
    array_of_dicts_with_multiple_items,
    business_validation_service,
):
    error_message = "Key at index 1 should be 'expected_key'"
    rule_for_array = rule_object_factory(
        array_of_dicts_with_multiple_items.field_code, array_of_dicts_with_multiple_items.document_type_code
    )
    rule_for_array.rule = rule
    rule_for_array.severity = "error"
    rule_for_array.issue_message = error_message

    validation_result = business_validation_service.validate([array_of_dicts_with_multiple_items], [rule_for_array])
    assert validation_result.is_valid is False
    assert len(validation_result.detail) == 1
    assert len(validation_result.detail[0].errors) > 0

    errors_with_index = [e for e in validation_result.detail[0].errors if e.index is not None]
    assert len(errors_with_index) > 0
    error = errors_with_index[0]

    assert error.index == 1
    assert error.kv_id == KeyValueId.KEY
    assert error.message == error_message
    assert error.column is None
    assert error.row is None


@pytest.mark.parametrize(
    "rule",
    [
        "Farray_dicts[1][1] == 'expected_value'",
    ],
)
def test_validate_array_of_dicts__value_validation__reports_index_and_kv_id_value(
    rule,
    rule_object_factory,
    array_of_dicts_with_multiple_items,
    business_validation_service,
):
    error_message = "Value at index 1 should be 'expected_value'"
    rule_for_array = rule_object_factory(
        array_of_dicts_with_multiple_items.field_code, array_of_dicts_with_multiple_items.document_type_code
    )
    rule_for_array.rule = rule
    rule_for_array.severity = "error"
    rule_for_array.issue_message = error_message

    validation_result = business_validation_service.validate([array_of_dicts_with_multiple_items], [rule_for_array])

    assert validation_result.is_valid is False
    assert len(validation_result.detail) == 1
    assert len(validation_result.detail[0].errors) > 0

    errors_with_index = [e for e in validation_result.detail[0].errors if e.index is not None]
    assert len(errors_with_index) > 0
    error = errors_with_index[0]

    assert error.index == 1
    assert error.kv_id == KeyValueId.VALUE
    assert error.message == error_message
    assert error.column is None
    assert error.row is None


@pytest.mark.parametrize(
    "rule",
    [
        "Fitem_of__array_dicts__0 == 'expected_key'",
    ],
)
def test_validate_array_of_dicts__every_key_validation__reports_index_and_kv_id_key(
    rule,
    rule_object_factory,
    array_of_dicts_with_multiple_items,
    business_validation_service,
):
    error_message = "Each item's key should be 'expected_key'"
    rule_for_array = rule_object_factory(
        array_of_dicts_with_multiple_items.field_code, array_of_dicts_with_multiple_items.document_type_code
    )
    rule_for_array.rule = rule
    rule_for_array.severity = "error"
    rule_for_array.issue_message = error_message
    rule_for_array.meta.for_each = True

    validation_result = business_validation_service.validate([array_of_dicts_with_multiple_items], [rule_for_array])

    assert validation_result.is_valid is False
    assert len(validation_result.detail) == 1
    assert len(validation_result.detail[0].errors) > 0

    errors_with_index = [e for e in validation_result.detail[0].errors if e.index is not None]
    assert len(errors_with_index) > 0
    error = errors_with_index[0]

    assert error.index == 0
    assert error.kv_id == KeyValueId.KEY
    assert error.message == error_message
    assert error.column is None
    assert error.row is None


@pytest.mark.parametrize(
    "rule",
    [
        "Fitem_of__array_dicts__1 == 'expected_value'",
    ],
)
def test_validate_array_of_dicts__every_value_validation__reports_index_and_kv_id_value(
    rule,
    rule_object_factory,
    array_of_dicts_with_multiple_items,
    business_validation_service,
):
    error_message = "Each item's value should be 'expected_value'"
    rule_for_array = rule_object_factory(
        array_of_dicts_with_multiple_items.field_code, array_of_dicts_with_multiple_items.document_type_code
    )
    rule_for_array.rule = rule
    rule_for_array.severity = "error"
    rule_for_array.issue_message = error_message
    rule_for_array.meta.for_each = True

    validation_result = business_validation_service.validate([array_of_dicts_with_multiple_items], [rule_for_array])

    assert validation_result.is_valid is False
    assert len(validation_result.detail) == 1
    assert len(validation_result.detail[0].errors) > 0

    errors_with_index = [e for e in validation_result.detail[0].errors if e.index is not None]
    assert len(errors_with_index) > 0
    error = errors_with_index[0]

    assert error.index == 0
    assert error.kv_id == KeyValueId.VALUE
    assert error.message == error_message
    assert error.column is None
    assert error.row is None
