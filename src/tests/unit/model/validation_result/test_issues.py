import pytest

from deps_high_sparrow.domain.model import Issues


@pytest.mark.issues
def test_create_extended__add_error_and_warning__counts_up(
    validation_issues, error_validation_issue, warning_validation_issue
):
    errors_count = len(validation_issues.errors)
    warnings_count = len(validation_issues.warnings)

    new_validation_issues = Issues(
        code=validation_issues.code,
        errors=[error_validation_issue],
        warnings=[warning_validation_issue],
    )

    updated_issues = validation_issues.create_extended(new_validation_issues)

    assert len(updated_issues.errors) == errors_count + 1
    assert len(updated_issues.warnings) == warnings_count + 1


@pytest.mark.issues
def test_create_extended__empty_new__unchanged(validation_issues):
    errors_count = len(validation_issues.errors)
    warnings_count = len(validation_issues.warnings)

    new_validation_issues = Issues(
        code=validation_issues.code,
        errors=[],
        warnings=[],
    )

    updated_issues = validation_issues.create_extended(new_validation_issues)

    assert len(updated_issues.errors) == errors_count
    assert len(updated_issues.warnings) == warnings_count
