from typing import Optional

from ...shared import EntityCode, Guard, ImmutableCheck
from .cross_field_issue import CrossFieldIssue

__all__ = ["CrossFieldIssues"]


class CrossFieldIssues:
    code = Guard[EntityCode](EntityCode, ImmutableCheck())
    errors = Guard[list[CrossFieldIssue]](list, ImmutableCheck())
    warnings = Guard[list[CrossFieldIssue]](list, ImmutableCheck())

    def __init__(
        self,
        code: EntityCode,
        errors: Optional[list[CrossFieldIssue]] = None,
        warnings: Optional[list[CrossFieldIssue]] = None,
    ) -> None:
        self.code = code

        self.errors = errors or []
        self.warnings = warnings or []

    def __call__(self) -> list[CrossFieldIssue]:
        return self.errors + self.warnings

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, self.__class__)
            and self.code == other.code
            and self.errors == other.errors
            and self.warnings == other.warnings
        )

    @property
    def is_valid(self) -> bool:
        return not self.errors

    def create_extended(self, cross_field_issues: "CrossFieldIssues") -> "CrossFieldIssues":
        return CrossFieldIssues(
            code=self.code,
            errors=[*self.errors, *cross_field_issues.errors],
            warnings=[*self.warnings, *cross_field_issues.warnings],
        )
