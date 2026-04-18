import pytest

from deps_high_sparrow.domain.exceptions import (
    RuleFieldReferencesMismatchError,
    UnparseableRuleError,
)
from deps_high_sparrow.domain.model.document_type import CrossFieldValidator
from deps_high_sparrow.domain.model.document_type.validator.validation.entities.constants import (
    KeyValueId,
)
from deps_high_sparrow.domain.model.document_type.validator.validation.services.utils import (
    FieldValidationIssues,
    Message,
)
from deps_high_sparrow.domain.model.shared import EntityCode, Severity
from deps_high_sparrow.domain.model.validation_result import CrossFieldIssueMessage


def test_cross_field_validator_make__valid_parameters__succeeds(
    cross_field_validator_id,
    cross_field_validator_name,
    cross_field_validator_description,
    cross_field_validator_rule,
    cross_field_validator_severity,
    cross_field_validated_fields,
    cross_field_issue_message_fixture,
):
    validator = CrossFieldValidator.make(
        id_=cross_field_validator_id,
        name=cross_field_validator_name,
        description=cross_field_validator_description,
        rule=cross_field_validator_rule,
        severity=cross_field_validator_severity,
        validated_fields=[f.value for f in cross_field_validated_fields],
        issue_message=cross_field_issue_message_fixture.message,
        dependent_fields=[f.value for f in cross_field_issue_message_fixture.dependent_fields],
    )

    assert validator.id() == cross_field_validator_id
    assert validator.name == cross_field_validator_name
    assert validator.description == cross_field_validator_description
    assert validator.rule == cross_field_validator_rule
    assert validator.severity == cross_field_validator_severity
    assert validator.validated_fields == cross_field_validated_fields
    assert validator.issue_message == cross_field_issue_message_fixture
    assert validator.for_each is False
    assert validator.for_any is False


def test_cross_field_validator_equality__same_id__equal(cross_field_validator):
    validator2 = CrossFieldValidator(
        id_=cross_field_validator.id(),
        name="different_name",
        description="different_description",
        rule="Fdifferent_field > 0",
        severity=Severity.WARNING,
        validated_fields=[EntityCode("different_field")],
        issue_message=CrossFieldIssueMessage(
            message="different_message",
            dependent_fields=[EntityCode("different_field")],
        ),
    )

    assert cross_field_validator == validator2


def test_cross_field_validator_equality__different_id__not_equal(cross_field_validator):
    validator2 = CrossFieldValidator(
        id_="different_id",
        name=cross_field_validator.name,
        description=cross_field_validator.description,
        rule=cross_field_validator.rule,
        severity=cross_field_validator.severity,
        validated_fields=cross_field_validator.validated_fields,
        issue_message=cross_field_validator.issue_message,
    )

    assert cross_field_validator != validator2


def test_get_position_from_issue__list_index__returns_position(cross_field_validator):
    message = Message(message="err", index=2)

    position = cross_field_validator._get_position_from_issue(message)

    assert position is not None
    assert position.index == 2
    assert position.column is None
    assert position.row is None
    assert position.kv_id is None


def test_get_position_from_issue__kv_id_and_index__returns_position(cross_field_validator):
    message = Message(
        message="warn",
        kv_id=KeyValueId.KEY,
        index=1,
    )

    position = cross_field_validator._get_position_from_issue(message)

    assert position is not None
    assert position.index == 1
    assert position.kv_id == KeyValueId.KEY.value
    assert position.column is None
    assert position.row is None


def test_get_position_from_issue__index_zero__returns_position(cross_field_validator):
    message = Message(message="err", index=0)

    position = cross_field_validator._get_position_from_issue(message)

    assert position is not None
    assert position.index == 0
    assert position.column is None
    assert position.row is None
    assert position.kv_id is None


def test_get_position_from_issue__kv_id_plain_value__returns_position(cross_field_validator):
    message = Message(message="err", kv_id="custom_key", index=0)

    position = cross_field_validator._get_position_from_issue(message)

    assert position is not None
    assert position.kv_id == "custom_key"
    assert position.index == 0
    assert position.column is None
    assert position.row is None


def test_get_position_from_issue__row_and_column_zero__returns_position(cross_field_validator):
    message = Message(message="err", column=0, row=0)

    position = cross_field_validator._get_position_from_issue(message)

    assert position is not None
    assert position.column == 0
    assert position.row == 0
    assert position.index is None
    assert position.kv_id is None


def test_get_position_from_issue__no_position_info__returns_none(cross_field_validator):
    message = Message(message="err")

    position = cross_field_validator._get_position_from_issue(message)

    assert position is None


def test_build_cross_field_issues__multiple_messages__returns_all_positions(cross_field_validator):
    issue = FieldValidationIssues(
        field_code="string_list_1",
        document_id=1,
        errors=[
            Message(message="first", index=5),
            Message(message="second", index=10),
            Message(message="third", index=15),
        ],
    )
    validated_fields_str = ["field1", "field2"]

    cross_field_issues = cross_field_validator._build_cross_field_issues(issue, validated_fields_str)

    assert len(cross_field_issues.errors) == 3
    assert len(cross_field_issues.warnings) == 0
    assert cross_field_issues.errors[0].position.index == 5
    assert cross_field_issues.errors[1].position.index == 10
    assert cross_field_issues.errors[2].position.index == 15
    assert all(e.severity == Severity.ERROR for e in cross_field_issues.errors)


def test_build_cross_field_issues__warning_severity__all_go_to_warnings(
    cross_field_validator_name,
    cross_field_validator_description,
    cross_field_validator_rule,
    cross_field_validated_fields,
    cross_field_issue_message_fixture,
):
    warning_validator = CrossFieldValidator(
        id_="warning_validator_id",
        name=cross_field_validator_name,
        description=cross_field_validator_description,
        rule=cross_field_validator_rule,
        severity=Severity.WARNING,
        validated_fields=cross_field_validated_fields,
        issue_message=cross_field_issue_message_fixture,
    )
    issue = FieldValidationIssues(
        field_code="table_field",
        document_id=1,
        warnings=[
            Message(message="warn1", column=0, row=0),
            Message(message="warn2", column=1, row=2),
        ],
    )
    validated_fields_str = ["field1"]

    cross_field_issues = warning_validator._build_cross_field_issues(issue, validated_fields_str)

    assert len(cross_field_issues.errors) == 0
    assert len(cross_field_issues.warnings) == 2
    assert cross_field_issues.warnings[0].position.column == 0
    assert cross_field_issues.warnings[0].position.row == 0
    assert cross_field_issues.warnings[1].position.column == 1
    assert cross_field_issues.warnings[1].position.row == 2
    assert all(w.severity == Severity.WARNING for w in cross_field_issues.warnings)


def test_build_cross_field_issues__mixed_sources__uses_validator_severity(cross_field_validator):
    issue = FieldValidationIssues(
        field_code="mixed_field",
        document_id=1,
        errors=[
            Message(message="err1", index=1),
            Message(message="err2", index=2),
        ],
        warnings=[
            Message(message="warn1", index=3),
        ],
    )
    validated_fields_str = ["field1", "field2"]

    cross_field_issues = cross_field_validator._build_cross_field_issues(issue, validated_fields_str)

    assert len(cross_field_issues.errors) == 3
    assert len(cross_field_issues.warnings) == 0
    assert cross_field_issues.errors[0].position.index == 1
    assert cross_field_issues.errors[1].position.index == 2
    assert cross_field_issues.errors[2].position.index == 3


def test_cross_field_validator_make__rule_references_unknown_field__raises(
    cross_field_validator_name,
    cross_field_validator_description,
    cross_field_validator_severity,
    cross_field_issue_message_fixture,
):
    with pytest.raises(RuleFieldReferencesMismatchError):
        CrossFieldValidator.make(
            id_="some_id",
            name=cross_field_validator_name,
            description=cross_field_validator_description,
            rule="Funknown > 0",
            severity=cross_field_validator_severity,
            validated_fields=["field1"],
            issue_message=cross_field_issue_message_fixture.message,
            dependent_fields=[f.value for f in cross_field_issue_message_fixture.dependent_fields],
        )


def test_cross_field_validator_update__rule_references_unknown_field__raises(cross_field_validator):
    with pytest.raises(RuleFieldReferencesMismatchError):
        cross_field_validator.update(
            name=cross_field_validator.name,
            description=cross_field_validator.description,
            rule="Funknown > 0",
            severity=cross_field_validator.severity,
            validated_fields=[EntityCode("field1")],
            issue_message=cross_field_validator.issue_message,
        )


def test_cross_field_validator_make__declared_field_missing_from_rule__raises(
    cross_field_validator_name,
    cross_field_validator_description,
    cross_field_validator_severity,
    cross_field_issue_message_fixture,
):
    with pytest.raises(RuleFieldReferencesMismatchError):
        CrossFieldValidator.make(
            id_="some_id",
            name=cross_field_validator_name,
            description=cross_field_validator_description,
            rule="Ffield1 > 0",
            severity=cross_field_validator_severity,
            validated_fields=["field1", "field2"],
            issue_message=cross_field_issue_message_fixture.message,
            dependent_fields=[f.value for f in cross_field_issue_message_fixture.dependent_fields],
        )


def test_cross_field_validator_update__declared_field_missing_from_rule__raises(cross_field_validator):
    with pytest.raises(RuleFieldReferencesMismatchError):
        cross_field_validator.update(
            name=cross_field_validator.name,
            description=cross_field_validator.description,
            rule="Ffield1 > 0",
            severity=cross_field_validator.severity,
            validated_fields=[EntityCode("field1"), EntityCode("field2")],
            issue_message=cross_field_validator.issue_message,
        )


def test_cross_field_validator_make__unparseable_rule__raises(
    cross_field_validator_name,
    cross_field_validator_description,
    cross_field_validator_severity,
    cross_field_issue_message_fixture,
    cross_field_validated_fields,
):
    with pytest.raises(UnparseableRuleError):
        CrossFieldValidator.make(
            id_="some_id",
            name=cross_field_validator_name,
            description=cross_field_validator_description,
            rule="Ffield1 +",
            severity=cross_field_validator_severity,
            validated_fields=[f.value for f in cross_field_validated_fields],
            issue_message=cross_field_issue_message_fixture.message,
            dependent_fields=[f.value for f in cross_field_issue_message_fixture.dependent_fields],
        )


def test_cross_field_validator_update__unparseable_rule__raises(cross_field_validator):
    with pytest.raises(UnparseableRuleError):
        cross_field_validator.update(
            name=cross_field_validator.name,
            description=cross_field_validator.description,
            rule="Ffield1 +",
            severity=cross_field_validator.severity,
            validated_fields=cross_field_validator.validated_fields,
            issue_message=cross_field_validator.issue_message,
        )


def test_build_cross_field_issues__no_messages__creates_issue_without_position(cross_field_validator):
    issue = FieldValidationIssues(
        field_code="empty_field",
        document_id=1,
        errors=[],
        warnings=[],
    )
    validated_fields_str = ["field1"]

    cross_field_issues = cross_field_validator._build_cross_field_issues(issue, validated_fields_str)

    assert len(cross_field_issues.errors) == 1
    assert len(cross_field_issues.warnings) == 0
    assert cross_field_issues.errors[0].position is None
