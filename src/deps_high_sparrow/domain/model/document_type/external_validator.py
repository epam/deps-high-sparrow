from ..shared import (
    EntityCode,
    FormatCheck,
    Guard,
    HttpUrlCheck,
    ImmutableCheck,
    LengthCheck,
    Severity,
)
from ..validation_result import Issue, Issues, IssueType, RawIssues

__all__ = ["ExternalValidator"]


class ExternalValidator:
    name = Guard[str](str, ImmutableCheck(), LengthCheck(min_length=1, max_length=100), FormatCheck("^[a-zA-Z0-9_-]+$"))
    url = Guard[str](str, ImmutableCheck(), HttpUrlCheck())

    def __init__(self, name: str, url: str) -> None:
        self.name = name
        self.url = url

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.name == other.name and self.url == other.url

    def validate(self, raw_issues_list: list[RawIssues]) -> list[Issues]:
        issues_list: list[Issues] = []

        for raw_issues in raw_issues_list:
            errors = [self._create_issue(error) for error in raw_issues["errors"] or []]
            warnings = [self._create_issue(warning) for warning in raw_issues["warnings"] or []]

            issues = Issues(code=EntityCode(raw_issues["code"]), errors=errors, warnings=warnings)
            issues_list.append(issues)

        return issues_list

    def _create_issue(self, raw_issue) -> Issue:
        raw_position = raw_issue.get("position")

        return Issue.from_message(
            severity=Severity(raw_issue["severity"]),
            type=IssueType.EXTERNAL_CHECK,
            message=raw_issue["message"],
            **raw_position if raw_position is not None else {},
        )
