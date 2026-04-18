from typing import Literal, TypedDict

__all__ = ["RawIssue"]


class RawIssue(TypedDict):
    message: str
    column: int
    row: int
    index: int
    kv_id: Literal["key", "value"]
