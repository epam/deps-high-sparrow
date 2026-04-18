from deps_high_sparrow.domain.model.shared import EntityCode, Severity
from deps_high_sparrow.domain.model.validation_result import CrossFieldIssueMessage
from deps_high_sparrow.infrastructure.repositories.document_type.mappers.cross_field_issue_message import (
    CrossFieldIssueMessageMapper,
)
from deps_high_sparrow.infrastructure.repositories.document_type.mappers.cross_field_validator import (
    CrossFieldValidatorMapper,
)


def test_cross_field_issue_message_mapper__to_dict__correct_structure(cross_field_issue_message):
    result = CrossFieldIssueMessageMapper.to_dict(cross_field_issue_message)

    assert isinstance(result, dict)
    assert result["message"] == cross_field_issue_message.message
    assert result["dependent_fields"] == [field.value for field in cross_field_issue_message.dependent_fields]


def test_cross_field_issue_message_mapper__from_dict__correct_object():
    raw_message = {
        "message": "Test message",
        "dependent_fields": ["field1", "field2"],
    }

    result = CrossFieldIssueMessageMapper.from_dict(raw_message)

    assert isinstance(result, CrossFieldIssueMessage)
    assert result.message == raw_message["message"]
    assert [field.value for field in result.dependent_fields] == raw_message["dependent_fields"]


def test_cross_field_validator_mapper__to_dict__correct_structure(cross_field_validator):
    result = CrossFieldValidatorMapper.to_dict(cross_field_validator)

    assert isinstance(result, dict)
    assert result["id"] == cross_field_validator.id()
    assert result["name"] == cross_field_validator.name
    assert result["description"] == cross_field_validator.description
    assert result["rule"] == cross_field_validator.rule
    assert result["severity"] == cross_field_validator.severity.value
    assert result["validated_fields"] == [field.value for field in cross_field_validator.validated_fields]
    assert "issue_message" in result
    assert result["for_each"] == cross_field_validator.for_each
    assert result["for_any"] == cross_field_validator.for_any


def test_cross_field_validator_mapper__from_dict__correct_object():
    raw_validator = {
        "id": "test_id",
        "name": "test_name",
        "description": "test_description",
        "rule": "Ffield1 == Ffield2",
        "severity": "error",
        "validated_fields": ["field1", "field2"],
        "issue_message": {
            "message": "Test message",
            "dependent_fields": ["field1", "field2"],
        },
        "for_each": True,
        "for_any": False,
    }

    result = CrossFieldValidatorMapper.from_dict(raw_validator)

    assert result.id() == raw_validator["id"]
    assert result.name == raw_validator["name"]
    assert result.description == raw_validator["description"]
    assert result.rule == raw_validator["rule"]
    assert result.severity == Severity.ERROR
    assert [field.value for field in result.validated_fields] == raw_validator["validated_fields"]
    assert result.issue_message.message == raw_validator["issue_message"]["message"]
    assert [field.value for field in result.issue_message.dependent_fields] == raw_validator["issue_message"][
        "dependent_fields"
    ]
    assert result.for_each == raw_validator["for_each"]
    assert result.for_any == raw_validator["for_any"]
