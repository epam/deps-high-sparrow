import pytest

from deps_high_sparrow.domain.model.document_type.validator.validation.entities.constants import (
    KeyValueId,
)


@pytest.mark.parametrize(
    "rule",
    [
        "Ffield_code5__0 == 'wrong_key'",
        "Ffield_code5[0] == 'wrong_key'",
    ],
)
def test_validate_dict__modern_format_key__reports_kv_id_key(
    rule,
    prepared_dict_field,
    business_validation_service,
    rule_object_factory,
):
    rule_obj = rule_object_factory(
        field_code=prepared_dict_field.field_code,
        document_type_code=prepared_dict_field.document_type_code,
    )
    rule_obj.rule = rule
    rule_obj.severity = "error"
    rule_obj.issue_message = "Key validation failed"

    validation_result = business_validation_service.validate([prepared_dict_field], [rule_obj])

    assert validation_result.is_valid is False
    assert len(validation_result.detail) == 1
    assert len(validation_result.detail[0].errors) > 0

    error = validation_result.detail[0].errors[0]
    assert error.kv_id == KeyValueId.KEY


@pytest.mark.parametrize(
    "rule",
    [
        "Ffield_code5__1 == 'wrong_value'",
        "Ffield_code5[1] == 'wrong_value'",
    ],
)
def test_validate_dict__modern_format_value__reports_kv_id_value(
    rule,
    prepared_dict_field,
    business_validation_service,
    rule_object_factory,
):
    rule_obj = rule_object_factory(
        field_code=prepared_dict_field.field_code,
        document_type_code=prepared_dict_field.document_type_code,
    )
    rule_obj.rule = rule
    rule_obj.severity = "error"
    rule_obj.issue_message = "Value validation failed"

    validation_result = business_validation_service.validate([prepared_dict_field], [rule_obj])

    assert validation_result.is_valid is False
    assert len(validation_result.detail) == 1
    assert len(validation_result.detail[0].errors) > 0

    error = validation_result.detail[0].errors[0]
    assert error.kv_id == KeyValueId.VALUE
