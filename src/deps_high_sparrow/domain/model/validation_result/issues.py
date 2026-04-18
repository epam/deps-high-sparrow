from typing import Optional

from ..shared import EntityCode, Guard, ImmutableCheck, Severity
from .issue import Issue, IssueType
from .raw_issue import RawIssue

__all__ = ["Issues"]


class Issues:
    code = Guard[EntityCode](EntityCode, ImmutableCheck())
    errors = Guard[list[Issue]](list, ImmutableCheck())
    warnings = Guard[list[Issue]](list, ImmutableCheck())

    def __init__(
        self,
        code: EntityCode,
        errors: Optional[list[Issue]] = None,
        warnings: Optional[list[Issue]] = None,
    ) -> None:
        self.code = code

        self.errors = errors or []
        self.warnings = warnings or []

    def __call__(self) -> list[Issue]:
        return self.errors + self.warnings

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, self.__class__)
            and self.code == other.code
            and self.errors == other.errors
            and self.warnings == other.warnings
        )

    def create_extended(self, issues: "Issues") -> "Issues":
        return Issues(
            code=self.code,
            errors=[*self.errors, *issues.errors],
            warnings=[*self.warnings, *issues.warnings],
        )

    @property
    def is_valid(self) -> bool:
        return not self.errors

    @property
    def has_pre_check_issues(self) -> bool:
        return any(filter(lambda issue: issue.type == IssueType.PRE_CHECK, self.errors)) or any(  # type: ignore
            filter(lambda issue: issue.type == IssueType.PRE_CHECK, self.warnings)  # type: ignore
        )

    @property
    def has_type_check_issues(self) -> bool:
        return any(filter(lambda issue: issue.type == IssueType.TYPE_CHECK, self.errors)) or any(  # type: ignore
            filter(lambda issue: issue.type == IssueType.TYPE_CHECK, self.warnings)  # type: ignore
        )

    @property
    def has_rules_check_issues(self) -> bool:
        return any(filter(lambda issue: issue.type == IssueType.RULES_CHECK, self.errors)) or any(  # type: ignore
            filter(lambda issue: issue.type == IssueType.RULES_CHECK, self.warnings)  # type: ignore
        )

    def add(self, type: IssueType, errors: list[RawIssue], warnings: list[RawIssue]) -> None:
        for error in errors:
            self.errors.append(Issue.from_message(severity=Severity.ERROR, type=type, **error))

        for warning in warnings:
            self.warnings.append(Issue.from_message(severity=Severity.WARNING, type=type, **warning))

    def add_pre_check_issues(self, errors: list[RawIssue], warnings: list[RawIssue]) -> None:
        self.add(IssueType.PRE_CHECK, errors, warnings)

    def add_type_check_issues(self, errors: list[RawIssue], warnings: list[RawIssue]) -> None:
        self.add(IssueType.TYPE_CHECK, errors, warnings)

    def add_rules_check_issues(self, errors: list[RawIssue], warnings: list[RawIssue]) -> None:
        self.add(IssueType.RULES_CHECK, errors, warnings)
