from typing import Any

from deps_high_sparrow.domain.model import CrossFieldValidator, EntityCode, Severity

from .cross_field_issue_message import CrossFieldIssueMessageMapper

__all__ = ["CrossFieldValidatorMapper"]


class CrossFieldValidatorMapper:
    @staticmethod
    def from_dict(raw_validator: dict[str, Any]) -> CrossFieldValidator:
        return CrossFieldValidator(
            id_=raw_validator["id"],
            name=raw_validator["name"],
            description=raw_validator["description"],
            rule=raw_validator["rule"],
            severity=Severity(raw_validator["severity"]),
            validated_fields=[EntityCode(field) for field in raw_validator["validated_fields"]],
            issue_message=CrossFieldIssueMessageMapper.from_dict(raw_validator["issue_message"]),
            for_each=raw_validator.get("for_each", False),
            for_any=raw_validator.get("for_any", False),
        )

    @staticmethod
    def to_dict(validator: CrossFieldValidator) -> dict[str, Any]:
        return {
            "id": validator.id(),
            "name": validator.name,
            "description": validator.description,
            "rule": validator.rule,
            "severity": validator.severity.value,
            "validated_fields": [field.value for field in validator.validated_fields],
            "issue_message": CrossFieldIssueMessageMapper.to_dict(validator.issue_message),
            "for_each": validator.for_each,
            "for_any": validator.for_any,
        }
