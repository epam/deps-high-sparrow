import pytest

from deps_high_sparrow.constants import MAX_LENGTH_DESCRIPTION_FIELD_VALIDATORS
from deps_high_sparrow.domain.exceptions import (
    ExternalValidatorAlreadyExistsError,
    MaxCrossFieldValidatorsExceededError,
    MaxExternalValidatorsExceededError,
)
from deps_high_sparrow.domain.model.shared import Severity


def test_remove_validator__unknown_code_empty_type__no_error(empty_document_type, field_code):
    empty_document_type.remove_validator(field_code)


def test_remove_validator__only_one_left__map_empty(document_type_with_string_validator, validator_code):
    assert document_type_with_string_validator._validators != {}

    document_type_with_string_validator.remove_validator(validator_code)

    assert document_type_with_string_validator._validators == {}


def test_remove_validator__four_total_drop_one__three_left(document_type_with_number_validator, validator_code):
    validator_codes = ["another1", "another2", "another3"]

    for code in validator_codes:
        document_type_with_number_validator.add_number_validator(code=code).is_required().build()

    assert len(document_type_with_number_validator._validators) == 4

    document_type_with_number_validator.remove_validator(validator_code)

    assert len(document_type_with_number_validator._validators) == 3
    assert validator_code not in document_type_with_number_validator._validators
    assert all(code in document_type_with_number_validator._validators for code in validator_codes)


@pytest.mark.document_type
def test_attach_external_validator__new__one_attached(
    document_type, external_validator_name, external_validator_url, external_validator
):
    document_type.attach_external_validator(name=external_validator_name, url=external_validator_url)

    assert len(document_type.external_validators) == 1
    assert document_type.external_validators[0] == external_validator


@pytest.mark.document_type
def test_attach_external_validator__duplicate_name__raises(
    document_type_with_external_validator,
    external_validator_name,
    external_validator_url,
):
    with pytest.raises(ExternalValidatorAlreadyExistsError):
        document_type_with_external_validator.attach_external_validator(
            name=external_validator_name, url=external_validator_url
        )


@pytest.mark.document_type
def test_attach_external_validator__at_limit__raises(
    document_type_with_maximum_external_validators,
    external_validator_name,
    external_validator_url,
):
    with pytest.raises(MaxExternalValidatorsExceededError):
        document_type_with_maximum_external_validators.attach_external_validator(
            name=external_validator_name, url=external_validator_url
        )


@pytest.mark.document_type
def test_remove_external_validator__existing_name__none_left(
    document_type_with_external_validator,
    external_validator_name,
):
    document_type_with_external_validator.remove_external_validator(external_validator_name)

    assert len(document_type_with_external_validator.external_validators) == 0


@pytest.mark.document_type
def test_add_cross_field_validator__valid_input__one_validator(
    document_type_with_validators,
    cross_field_validator_name,
    cross_field_validator_description,
    cross_field_validator_rule,
    cross_field_validator_severity,
    cross_field_validated_fields,
    cross_field_issue_message_text,
    cross_field_dependent_fields,
):
    validated_fields_str = [field.value for field in cross_field_validated_fields]
    dependent_fields_str = [field.value for field in cross_field_dependent_fields]

    validator_id = document_type_with_validators.add_cross_field_validator(
        name=cross_field_validator_name,
        description=cross_field_validator_description,
        rule=cross_field_validator_rule,
        severity=cross_field_validator_severity,
        validated_fields=validated_fields_str,
        issue_message=cross_field_issue_message_text,
        dependent_fields=dependent_fields_str,
    )

    assert validator_id is not None
    assert len(document_type_with_validators.cross_field_validators) == 1

    validator = document_type_with_validators.cross_field_validators[0]
    assert validator.id() == validator_id
    assert validator.name == cross_field_validator_name
    assert validator.description == cross_field_validator_description
    assert validator.rule == cross_field_validator_rule
    assert validator.severity == cross_field_validator_severity
    assert [field.value for field in validator.validated_fields] == validated_fields_str
    assert validator.issue_message.message == cross_field_issue_message_text
    assert [field.value for field in validator.issue_message.dependent_fields] == dependent_fields_str


@pytest.mark.document_type
def test_add_cross_field_validator__for_each_for_any__both_true(
    document_type_with_validators,
    cross_field_validator_name,
    cross_field_validator_description,
    cross_field_validator_rule,
    cross_field_validator_severity,
    cross_field_validated_fields,
    cross_field_issue_message_text,
    cross_field_dependent_fields,
):
    validated_fields_str = [field.value for field in cross_field_validated_fields]
    dependent_fields_str = [field.value for field in cross_field_dependent_fields]

    validator_id = document_type_with_validators.add_cross_field_validator(
        name=cross_field_validator_name,
        description=cross_field_validator_description,
        rule=cross_field_validator_rule,
        severity=cross_field_validator_severity,
        validated_fields=validated_fields_str,
        issue_message=cross_field_issue_message_text,
        dependent_fields=dependent_fields_str,
        for_each=True,
        for_any=True,
    )

    validator = document_type_with_validators.cross_field_validators[0]
    assert validator.id() == validator_id
    assert validator.for_each is True
    assert validator.for_any is True


@pytest.mark.document_type
def test_add_cross_field_validator__over_limit__raises(document_type_with_validators):
    for i in range(MAX_LENGTH_DESCRIPTION_FIELD_VALIDATORS):
        document_type_with_validators.add_cross_field_validator(
            name=f"validator_{i}",
            description=f"description_{i}",
            rule="Ffield1 > 0",
            severity=Severity.ERROR,
            validated_fields=["field1"],
            issue_message=f"message_{i} ${{field1}}",
            dependent_fields=["field1"],
        )

    with pytest.raises(MaxCrossFieldValidatorsExceededError):
        document_type_with_validators.add_cross_field_validator(
            name="one_too_many",
            description="description",
            rule="rule",
            severity=Severity.ERROR,
            validated_fields=["field1"],
            issue_message="message ${field1}",
            dependent_fields=["field1"],
        )


@pytest.mark.document_type
def test_cross_field_validators__three_added__len_three(document_type_with_validators):
    validator_ids = []
    for i in range(3):
        validator_id = document_type_with_validators.add_cross_field_validator(
            name=f"validator_{i}",
            description=f"description_{i}",
            rule="Ffield1 > 0",
            severity=Severity.ERROR,
            validated_fields=["field1"],
            issue_message=f"message_{i} ${{field1}}",
            dependent_fields=["field1"],
        )
        validator_ids.append(validator_id)

    validators = document_type_with_validators.cross_field_validators
    assert len(validators) == 3
    assert all(v.id() in validator_ids for v in validators)


@pytest.mark.document_type
def test_has_cross_field_validators__when_present__true(document_type_with_cross_field_validator):
    assert document_type_with_cross_field_validator.has_cross_field_validators is True


@pytest.mark.document_type
def test_has_cross_field_validators__when_empty__false(document_type):
    assert document_type.has_cross_field_validators is False


@pytest.mark.document_type
def test_update_cross_field_validator__new_values__matches(
    document_type_with_all_validators,
):
    document_type, cross_field_validator_id = document_type_with_all_validators
    expected_name = "new_validator_name"
    expected_description = "new_description"
    expected_rule = "newrule"
    expected_severity = Severity.WARNING
    expected_fields = []
    expected_issue_message = "newissuemessage"

    document_type.update_cross_field_validator(
        validator_id=cross_field_validator_id,
        name=expected_name,
        description=expected_description,
        rule=expected_rule,
        severity=expected_severity,
        validated_fields=expected_fields,
        issue_message=expected_issue_message,
        dependent_fields=expected_fields,
    )

    validator = document_type.cross_field_validators[0]

    assert validator.id() == cross_field_validator_id
    assert validator.name == expected_name
    assert validator.description == expected_description
    assert validator.rule == expected_rule
    assert validator.severity == expected_severity
    assert validator.validated_fields == expected_fields
    assert validator.issue_message.message == expected_issue_message
    assert validator.issue_message.dependent_fields == expected_fields


@pytest.mark.document_type
def test_fields_to_validate_with__no_cross_field_validators__returns_only_target_field(document_type):
    result = document_type.fields_to_validate_with("field1")

    assert result == ["field1"]


@pytest.mark.document_type
def test_fields_to_validate_with__field_in_cross_field_validator__returns_all_related_fields(
    document_type_with_all_validators,
):
    document_type, _ = document_type_with_all_validators

    result = document_type.fields_to_validate_with("field1")

    assert set(result) == {"field1", "field2"}


@pytest.mark.document_type
def test_fields_to_validate_with__multiple_cross_field_validators__returns_all_related_fields(
    document_type_with_validators,
):
    document_type_with_validators.add_cross_field_validator(
        name="validator_1",
        description="First validator",
        rule="Ffield1 == Ffield2",
        severity=Severity.ERROR,
        validated_fields=["field1"],
        issue_message="Fields must match ${field2}",
        dependent_fields=["field2"],
    )
    document_type_with_validators.add_string_validator(code="field3").is_required().build()
    document_type_with_validators.add_cross_field_validator(
        name="validator_2",
        description="Second validator",
        rule="Ffield1 > Ffield3",
        severity=Severity.WARNING,
        validated_fields=["field1"],
        issue_message="Field1 must be greater than ${field3}",
        dependent_fields=["field3"],
    )

    result = document_type_with_validators.fields_to_validate_with("field1")

    assert set(result) == {"field1", "field2", "field3"}
