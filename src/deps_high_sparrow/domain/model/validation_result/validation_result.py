from typing import Optional

from ...events import BusinessRuleViolated
from ..shared import EntityId, Guard, ImmutableCheck, TenantId
from .cross_field_issue import CrossFieldIssues
from .issue import IssueType
from .issues import Issues

__all__ = ["ValidationResult"]


class ValidationResult:
    id = Guard[EntityId](EntityId, ImmutableCheck())
    tenant_id = Guard[TenantId](TenantId, ImmutableCheck())

    def __init__(
        self,
        id: str,
        tenant_id: str,
        issues: Optional[list[Issues]] = None,
        cross_field_issues: Optional[list[CrossFieldIssues]] = None,
    ) -> None:
        self.id = EntityId(id)
        self.tenant_id = TenantId(tenant_id)

        self._issues: dict[str, Issues] = {} if issues is None else {issue.code(): issue for issue in issues}
        self._cross_field_issues: dict[str, CrossFieldIssues] = (
            {}
            if cross_field_issues is None
            else {cross_field_issue.code(): cross_field_issue for cross_field_issue in cross_field_issues}
        )
        self._events: list = []

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.id == other.id

    @property
    def issues(self) -> dict[str, Issues]:
        return self._issues

    @property
    def cross_field_issues(self) -> dict[str, CrossFieldIssues]:
        return self._cross_field_issues

    @property
    def is_valid(self) -> bool:
        return all(issues.is_valid for issues in self._issues.values()) and all(
            cross_field_issues.is_valid for cross_field_issues in self._cross_field_issues.values()
        )

    @property
    def events(self) -> list:
        return self._events

    def add_issues(self, issues: Issues) -> None:
        if existing_issues := self._issues.get(issues.code()):
            self._issues[issues.code()] = existing_issues.create_extended(issues)
        else:
            self._issues[issues.code()] = issues

        if issues.has_rules_check_issues:
            self._events.append(
                BusinessRuleViolated(
                    document_id=self.id(),
                    field_code=issues.code(),
                    message="; ".join(
                        [issue.message for issue in issues() if issue.type == IssueType.RULES_CHECK],
                    ),
                )
            )

    def replace_issues(self, issues: Issues) -> None:
        self._issues[issues.code()] = issues

    def add_cross_field_issues(self, cross_field_issues: CrossFieldIssues) -> None:
        if existing_issues := self._cross_field_issues.get(cross_field_issues.code.value):
            self._cross_field_issues[cross_field_issues.code()] = existing_issues.create_extended(cross_field_issues)
        else:
            self._cross_field_issues[cross_field_issues.code()] = cross_field_issues

        for cross_field_issue in cross_field_issues():
            self._events.append(
                BusinessRuleViolated(
                    document_id=self.id(),
                    field_code=cross_field_issue.code.value,
                    message=cross_field_issue.message.message,
                )
            )

    def replace_cross_field_issues(self, cross_field_issues: CrossFieldIssues) -> None:
        self._cross_field_issues[cross_field_issues.code()] = cross_field_issues
