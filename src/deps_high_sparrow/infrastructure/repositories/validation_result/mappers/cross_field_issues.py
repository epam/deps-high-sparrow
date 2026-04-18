from typing import Any

from deps_high_sparrow.domain import CrossFieldIssues, EntityCode

from .cross_field_issue import CrossFieldIssueMapper

__all__ = ["CrossFieldIssuesMapper"]


class CrossFieldIssuesMapper:
    @staticmethod
    def to_dict(issues: CrossFieldIssues) -> dict[str, Any]:
        return {
            "code": issues.code.value,
            "errors": [CrossFieldIssueMapper.to_dict(error) for error in issues.errors],
            "warnings": [CrossFieldIssueMapper.to_dict(warning) for warning in issues.warnings],
        }

    @staticmethod
    def from_dict(raw_issues: dict[str, Any]) -> CrossFieldIssues:
        return CrossFieldIssues(
            code=EntityCode(raw_issues["code"]),
            errors=[CrossFieldIssueMapper.from_dict(error) for error in raw_issues["errors"]],
            warnings=[CrossFieldIssueMapper.from_dict(warning) for warning in raw_issues["warnings"]],
        )
