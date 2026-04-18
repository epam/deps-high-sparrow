from deps_high_sparrow.domain.model import IssueType, Severity


def test_replace_issues__after_type_check__only_pre_check(
    validation_result_type_check_only,
    issues_pre_check,
):
    validation_result_type_check_only.replace_issues(issues_pre_check)

    final_issues = validation_result_type_check_only.issues[issues_pre_check.code()]

    assert len(final_issues()) == 1
    assert final_issues()[0].type == IssueType.PRE_CHECK


def test_replace_cross_field_issues__after_error__only_warning(
    validation_result_cross_error_only,
    cross_issues_warning,
):
    validation_result_cross_error_only.replace_cross_field_issues(cross_issues_warning)

    final = validation_result_cross_error_only.cross_field_issues[cross_issues_warning.code()]

    assert len(final.errors) == 0
    assert len(final()) == 1
    assert final.warnings[0].severity == Severity.WARNING
    assert final.warnings[0].message.message == "Cross warning"
