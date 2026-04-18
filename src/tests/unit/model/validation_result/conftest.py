from uuid import uuid4

import pytest

from deps_high_sparrow.domain.model import (
    CrossFieldIssue,
    CrossFieldIssueMessage,
    CrossFieldIssues,
    EntityCode,
    Issues,
    IssueType,
    RawIssue,
    Severity,
)


@pytest.fixture
def field_code():
    return uuid4().hex


@pytest.fixture
def issues_type_check(field_code):
    issues = Issues(code=EntityCode(field_code))
    issues.add(
        type=IssueType.TYPE_CHECK,
        errors=[
            RawIssue(
                message="Type error",
                column=None,
                row=None,
                index=None,
                kv_id=None,
            )
        ],
        warnings=[],
    )
    return issues


@pytest.fixture
def issues_pre_check(field_code):
    issues = Issues(code=EntityCode(field_code))
    issues.add(
        type=IssueType.PRE_CHECK,
        errors=[
            RawIssue(
                message="Pre-check error",
                column=None,
                row=None,
                index=None,
                kv_id=None,
            )
        ],
        warnings=[],
    )
    return issues


@pytest.fixture
def validation_result_type_check_only(validation_result, issues_type_check):
    validation_result.add_issues(issues_type_check)
    existing = validation_result.issues[issues_type_check.code()]
    assert len(existing()) == 1
    assert existing()[0].type == IssueType.TYPE_CHECK
    return validation_result


@pytest.fixture
def cross_field_code():
    return uuid4().hex


@pytest.fixture
def cross_issues_error(cross_field_code):
    issue = CrossFieldIssue.from_message(
        code=cross_field_code,
        validator_id=uuid4().hex,
        severity=Severity.ERROR,
        message=CrossFieldIssueMessage("Cross error", dependent_fields=[]),
        validated_fields=[cross_field_code],
    )
    return CrossFieldIssues(code=EntityCode(cross_field_code), errors=[issue])


@pytest.fixture
def cross_issues_warning(cross_field_code):
    issue = CrossFieldIssue.from_message(
        code=cross_field_code,
        validator_id=uuid4().hex,
        severity=Severity.WARNING,
        message=CrossFieldIssueMessage("Cross warning", dependent_fields=[]),
        validated_fields=[cross_field_code],
    )
    return CrossFieldIssues(code=EntityCode(cross_field_code), warnings=[issue])


@pytest.fixture
def validation_result_cross_error_only(validation_result, cross_issues_error):
    validation_result.add_cross_field_issues(cross_issues_error)
    existing = validation_result.cross_field_issues[cross_issues_error.code()]
    assert len(existing()) == 1
    assert existing.errors[0].severity == Severity.ERROR
    return validation_result
