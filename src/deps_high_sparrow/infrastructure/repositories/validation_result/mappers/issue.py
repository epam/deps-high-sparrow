from typing import Any

from deps_high_sparrow.domain import Issue, IssueType, Severity

from .position import PositionMapper

__all__ = ["IssueMapper"]


class IssueMapper:
    @staticmethod
    def to_dict(issue: Issue) -> dict[str, Any]:
        raw_position = PositionMapper.to_dict(issue.position) if issue.position else {}

        return {
            "severity": issue.severity.value,
            "type": issue.type.value,
            "message": issue.message,
            **raw_position,
        }

    @staticmethod
    def from_dict(raw_issue: dict[str, Any]) -> Issue:
        return Issue.from_message(
            severity=Severity(raw_issue["severity"]),
            type=IssueType(raw_issue["type"]),
            message=raw_issue["message"],
            column=raw_issue.get("column"),
            row=raw_issue.get("row"),
            index=raw_issue.get("index"),
            kv_id=raw_issue.get("kv_id"),
        )
