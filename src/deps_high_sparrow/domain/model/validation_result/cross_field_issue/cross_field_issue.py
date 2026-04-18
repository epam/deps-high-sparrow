from typing import Literal, Optional

from ...shared import EntityCode, EntityId, Guard, ImmutableCheck, Severity
from ..cross_field_issue_message import CrossFieldIssueMessage
from ..issue.position import Position

__all__ = ["CrossFieldIssue"]


class CrossFieldIssue:
    code = Guard[EntityCode](EntityCode, ImmutableCheck())
    validator_id = Guard[EntityId](EntityId, ImmutableCheck())
    severity = Guard[Severity](Severity, ImmutableCheck())
    validated_fields = Guard[list[str]](list)
    message = Guard[CrossFieldIssueMessage](CrossFieldIssueMessage, ImmutableCheck())
    position = Guard[Position](Position, ImmutableCheck())

    def __init__(
        self,
        code: EntityCode,
        validator_id: EntityId,
        severity: Severity,
        message: CrossFieldIssueMessage,
        validated_fields: Optional[list[str]] = None,
        position: Optional[Position] = None,
    ) -> None:
        self.code = code
        self.validator_id = validator_id
        self.severity = severity
        self.validated_fields = validated_fields if validated_fields else []
        self.message = message

        if position is not None:
            self.position = position

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, self.__class__)
            and self.code == other.code
            and self.validator_id == other.validator_id
            and self.severity == other.severity
            and self.validated_fields == other.validated_fields
            and self.message == other.message
            and self.position == other.position
        )

    @classmethod
    def from_message(
        cls,
        code: str,
        validator_id: str,
        severity: Severity,
        message: CrossFieldIssueMessage,
        validated_fields: list[str],
        column: Optional[int] = None,
        row: Optional[int] = None,
        index: Optional[int] = None,
        kv_id: Optional[Literal["key", "value"]] = None,
    ) -> "CrossFieldIssue":
        issue = cls(
            code=EntityCode(code),
            validator_id=EntityId(validator_id),
            severity=severity,
            message=message,
            validated_fields=validated_fields,
        )

        if column is not None and row is not None:
            issue.position = Position.for_cell(column, row, index=index)
        elif kv_id is not None:
            issue.position = Position.for_kv_id(kv_id, index=index)
        elif index is not None:
            issue.position = Position.for_list(index=index)

        return issue
