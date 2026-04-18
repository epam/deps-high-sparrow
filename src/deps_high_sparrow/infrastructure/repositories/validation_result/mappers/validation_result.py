from typing import Any

from deps_high_sparrow.domain import ValidationResult

from .cross_field_issues import CrossFieldIssuesMapper
from .issues import IssuesMapper

__all__ = ["ValidationResultMapper"]


class ValidationResultMapper:
    @staticmethod
    def to_dict(validation_result: ValidationResult) -> dict[str, Any]:
        raw_issues = [IssuesMapper.to_dict(issues) for issues in validation_result.issues.values()]
        raw_cross_field_issues = [
            CrossFieldIssuesMapper.to_dict(issues) for issues in validation_result.cross_field_issues.values()
        ]

        return {
            "id": validation_result.id.value,
            "tenant_id": validation_result.tenant_id.value,
            "issues": raw_issues or None,
            "cross_field_issues": raw_cross_field_issues or None,
        }

    @staticmethod
    def from_dict(raw_validation_result: dict[str, Any]) -> ValidationResult:
        issues = (
            [IssuesMapper.from_dict(raw_issues) for raw_issues in raw_validation_result["issues"]]
            if raw_validation_result["issues"]
            else []
        )
        cross_field_issues = (
            [CrossFieldIssuesMapper.from_dict(raw_issues) for raw_issues in raw_validation_result["cross_field_issues"]]
            if raw_validation_result["cross_field_issues"]
            else []
        )

        return ValidationResult(
            id=raw_validation_result["id"],
            tenant_id=raw_validation_result["tenant_id"],
            issues=issues,
            cross_field_issues=cross_field_issues,
        )
