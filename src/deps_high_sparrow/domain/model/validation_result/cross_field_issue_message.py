from typing import List

from deps_high_sparrow.domain.model.shared import EntityCode, Guard
from deps_high_sparrow.domain.model.shared.guards.checks import ImmutableCheck

__all__ = ["CrossFieldIssueMessage"]


class CrossFieldIssueMessage:
    message = Guard[str](str, ImmutableCheck())
    dependent_fields = Guard[List[EntityCode]](list, ImmutableCheck())

    def __init__(self, message: str, dependent_fields: List[EntityCode]) -> None:
        self.message = message
        self.dependent_fields = dependent_fields

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CrossFieldIssueMessage):
            return False
        return self.message == other.message and self.dependent_fields == other.dependent_fields

    def __repr__(self) -> str:
        return f"CrossFieldIssueMessage(message='{self.message}', dependent_fields={self.dependent_fields})"
