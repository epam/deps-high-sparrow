def test_record_field_validation__mismatched_values__field1_issues_and_cross_field(
    document_type_cross_rules,
    document_id,
    entity_code_1,
    entity_code_2,
    artifacts_two_fields,
):
    document_type_cross_rules.record_field_validation(
        document_id=document_id,
        field_code=entity_code_1,
        document_artifacts=artifacts_two_fields,
        validation_result=None,
    )

    validation_result = document_type_cross_rules.derive_validation_result()

    assert validation_result is not None
    assert validation_result.id() == document_id
    assert entity_code_1 in validation_result.issues
    assert entity_code_1 in validation_result.cross_field_issues
    assert entity_code_2 not in validation_result.cross_field_issues


def test_record_field_validation__valid_after_invalid__clears_same_result(
    document_type_field1_invalid,
    document_id,
    entity_code_1,
    validation_result_field1_one_issue,
    artifacts_field1_present,
):
    document_type_field1_invalid.record_field_validation(
        document_id=document_id,
        field_code=entity_code_1,
        document_artifacts=artifacts_field1_present,
        validation_result=validation_result_field1_one_issue,
    )

    final_result = document_type_field1_invalid.derive_validation_result()

    assert final_result is validation_result_field1_one_issue
    assert len(final_result.issues[entity_code_1]()) == 0


def test_record_field_validation__field1_after_field3__both_in_issues(
    document_type_field3_invalid,
    document_id,
    entity_code_1,
    entity_code_3,
    validation_result_field3_issues,
    artifacts_two_fields,
):
    document_type_field3_invalid.record_field_validation(
        document_id=document_id,
        field_code=entity_code_1,
        document_artifacts=artifacts_two_fields,
        validation_result=validation_result_field3_issues,
    )

    final_result = document_type_field3_invalid.derive_validation_result()

    assert final_result is validation_result_field3_issues
    assert entity_code_3 in final_result.issues
    assert entity_code_1 in final_result.issues


def test_record_field_validation__unknown_field__no_issues_for_code(
    document_type_cross_rules,
    document_id,
    unknown_field_code,
    artifacts_field1_only,
):
    document_type_cross_rules.record_field_validation(
        document_id=document_id,
        field_code=unknown_field_code,
        document_artifacts=artifacts_field1_only,
        validation_result=None,
    )

    validation_result = document_type_cross_rules.derive_validation_result()

    assert validation_result is not None
    assert unknown_field_code not in validation_result.issues


def test_record_field_validation__no_cross_rules__field_issues_only(
    document_type_string_only,
    document_id,
    entity_code_1,
    artifacts_field1_only,
):
    document_type_string_only.record_field_validation(
        document_id=document_id,
        field_code=entity_code_1,
        document_artifacts=artifacts_field1_only,
        validation_result=None,
    )

    validation_result = document_type_string_only.derive_validation_result()

    assert validation_result is not None
    assert entity_code_1 in validation_result.issues
    assert len(validation_result.cross_field_issues) == 0
