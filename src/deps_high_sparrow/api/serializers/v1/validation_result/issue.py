from typing import Optional

from pydantic import Field

from deps_high_sparrow.domain.model import Issue, IssueType, Severity

from ...base import ConfiguredBaseModel

__all__ = ["SerializedIssue"]


class SerializedIssue(ConfiguredBaseModel):
    severity: Severity
    type: IssueType
    message: str
    column: Optional[int]
    row: Optional[int]
    index: Optional[int]
    kv_id: Optional[str] = Field(alias="kvId")

    @classmethod
    def from_model(cls, issue: Issue) -> "SerializedIssue":
        return cls(
            severity=issue.severity,
            type=issue.type,
            message=issue.message,
            column=issue.position.column if issue.position else None,
            row=issue.position.row if issue.position else None,
            index=issue.position.index if issue.position else None,
            kv_id=issue.position.kv_id if issue.position else None,
        )
