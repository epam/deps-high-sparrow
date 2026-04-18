from typing import Any

from deps_high_sparrow.domain import EntityCode, Issues

from .issue import IssueMapper

__all__ = ["IssuesMapper"]


class IssuesMapper:
    @staticmethod
    def to_dict(issues: Issues) -> dict[str, Any]:
        return {
            "code": issues.code.value,
            "errors": [IssueMapper.to_dict(error) for error in issues.errors],
            "warnings": [IssueMapper.to_dict(warning) for warning in issues.warnings],
        }

    @staticmethod
    def from_dict(raw_issues: dict[str, Any]) -> Issues:
        return Issues(
            code=EntityCode(raw_issues["code"]),
            errors=[IssueMapper.from_dict(error) for error in raw_issues["errors"]],
            warnings=[IssueMapper.from_dict(warning) for warning in raw_issues["warnings"]],
        )
