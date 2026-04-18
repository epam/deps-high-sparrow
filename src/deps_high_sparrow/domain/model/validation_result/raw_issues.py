from typing import Optional, TypedDict

__all__ = ["RawIssues"]


class RawPosition(TypedDict):
    column: Optional[int]
    row: Optional[int]
    kv_id: Optional[str]
    index: Optional[int]


class RawIssue(TypedDict):
    severity: str
    type: str
    message: str
    position: Optional[RawPosition]


class RawIssues(TypedDict):
    code: str
    errors: Optional[list[RawIssue]]
    warnings: Optional[list[RawIssue]]
