from typing import Literal, Optional

from ...shared import Guard, ImmutableCheck, Severity
from .issue_type import IssueType
from .position import Position

__all__ = ["Issue"]


class Issue:
    severity = Guard[Severity](Severity, ImmutableCheck())
    type = Guard[IssueType](IssueType, ImmutableCheck())
    message = Guard[str](str, ImmutableCheck())
    position = Guard[Position](Position, ImmutableCheck())

    def __init__(
        self,
        severity: Severity,
        type: IssueType,
        message: str,
        position: Optional[Position] = None,
    ) -> None:
        self.severity = severity
        self.type = type
        self.message = message

        if position is not None:
            self.position = position

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, self.__class__)
            and self.severity == other.severity
            and self.type == other.type
            and self.message == other.message
            and self.position == other.position
        )

    @classmethod
    def from_message(
        cls,
        severity: Severity,
        type: IssueType,
        message: str,
        column: Optional[int] = None,
        row: Optional[int] = None,
        index: Optional[int] = None,
        kv_id: Optional[Literal["key", "value"]] = None,
    ) -> "Issue":
        issue = cls(severity=severity, type=type, message=message)

        if column is not None and row is not None:
            issue.position = Position.for_cell(column, row, index=index)
        elif kv_id is not None:
            issue.position = Position.for_kv_id(kv_id, index=index)
        elif index is not None:
            issue.position = Position.for_list(index=index)

        return issue
