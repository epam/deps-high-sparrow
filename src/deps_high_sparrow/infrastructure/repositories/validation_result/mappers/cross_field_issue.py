from typing import Any

from deps_high_sparrow.domain import CrossFieldIssue, Severity

from ...document_type.mappers.cross_field_issue_message import (
    CrossFieldIssueMessageMapper,
)
from .position import PositionMapper

__all__ = ["CrossFieldIssueMapper"]


class CrossFieldIssueMapper:
    @staticmethod
    def to_dict(cross_field_issue: CrossFieldIssue) -> dict[str, Any]:
        raw_position = PositionMapper.to_dict(cross_field_issue.position) if cross_field_issue.position else {}

        return {
            "code": cross_field_issue.code.value,
            "validator_id": cross_field_issue.validator_id.value,
            "severity": cross_field_issue.severity.value,
            "validated_fields": cross_field_issue.validated_fields,
            "message": CrossFieldIssueMessageMapper.to_dict(cross_field_issue.message),
            **raw_position,
        }

    @staticmethod
    def from_dict(raw_cross_field_issue: dict[str, Any]) -> CrossFieldIssue:
        return CrossFieldIssue.from_message(
            code=raw_cross_field_issue["code"],
            validator_id=raw_cross_field_issue["validator_id"],
            severity=Severity(raw_cross_field_issue["severity"]),
            validated_fields=raw_cross_field_issue["validated_fields"],
            message=CrossFieldIssueMessageMapper.from_dict(raw_cross_field_issue["message"]),
            column=raw_cross_field_issue.get("column"),
            row=raw_cross_field_issue.get("row"),
            index=raw_cross_field_issue.get("index"),
            kv_id=raw_cross_field_issue.get("kv_id"),
        )
