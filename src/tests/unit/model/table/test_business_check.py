from uuid import uuid4

import pytest

from deps_high_sparrow.domain.model import DocumentArtifact, DocumentType


@pytest.mark.model_business_check
def test_is_valid(
    document_id,
    entity_code_1,
    document_type: DocumentType,
    prepared_table_artifact: DocumentArtifact,
):
    error_message = uuid4().hex

    document_type.add_error_check_to_validator(
        entity_code_1,
        name=uuid4().hex,
        rule=f"type_code__{entity_code_1}__0 == 1",
        issue_message=error_message,
    )

    document_type.record_local_validation(document_id, [prepared_table_artifact])
    validation_result = document_type.derive_validation_result()

    assert validation_result.is_valid


@pytest.mark.model_business_check
def test_is_failed(
    document_id,
    entity_code_1,
    document_type: DocumentType,
    prepared_table_artifact: DocumentArtifact,
):
    error_message = uuid4().hex

    document_type.add_error_check_to_validator(
        entity_code_1,
        name=uuid4().hex,
        rule=f"type_code__{entity_code_1}__0 != 1",
        issue_message=error_message,
    )

    document_type.record_local_validation(document_id, [prepared_table_artifact])
    validation_result = document_type.derive_validation_result()

    assert not validation_result.is_valid

    issue_1 = validation_result.issues[entity_code_1].errors[0]
    assert issue_1.message == error_message
    assert (issue_1.position.column, issue_1.position.row) == (prepared_table_artifact.value[0][1])

    issue_2 = validation_result.issues[entity_code_1].errors[-1]
    assert issue_2.message == "Table contains errors"


@pytest.mark.model_business_check
def test_two_columns__is_valid(
    document_id,
    entity_code_1,
    document_type: DocumentType,
    prepared_table_artifact: DocumentArtifact,
):
    error_message = uuid4().hex

    document_type.add_error_check_to_validator(
        entity_code_1,
        name=uuid4().hex,
        rule=f"type_code__{entity_code_1}__0 < type_code__{entity_code_1}__2",
        issue_message=error_message,
    )

    document_type.record_local_validation(document_id, [prepared_table_artifact])
    validation_result = document_type.derive_validation_result()

    assert validation_result.is_valid


@pytest.mark.model_business_check
def test_two_columns__missed_optional_cell__is_valid(
    document_id,
    entity_code_1,
    empty_value,
    document_type: DocumentType,
    prepared_table_artifact: DocumentArtifact,
):
    error_message = uuid4().hex
    prepared_table_artifact.value[2][0] = empty_value

    document_type.add_error_check_to_validator(
        entity_code_1,
        name=uuid4().hex,
        rule=f"type_code__{entity_code_1}__0 < type_code__{entity_code_1}__2",
        issue_message=error_message,
        check_optional_fields=True,
    )

    document_type.record_local_validation(document_id, [prepared_table_artifact])
    validation_result = document_type.derive_validation_result()

    assert validation_result.is_valid


@pytest.mark.model_business_check
def test_two_columns__is_failed(
    document_id,
    entity_code_1,
    document_type: DocumentType,
    prepared_table_artifact: DocumentArtifact,
):
    error_message = uuid4().hex

    document_type.add_error_check_to_validator(
        entity_code_1,
        name=uuid4().hex,
        rule=f"type_code__{entity_code_1}__0 > type_code__{entity_code_1}__2",
        issue_message=error_message,
    )

    document_type.record_local_validation(document_id, [prepared_table_artifact])
    validation_result = document_type.derive_validation_result()

    assert not validation_result.is_valid

    issue_1 = validation_result.issues[entity_code_1].errors[0]
    assert issue_1.message == error_message
    assert (issue_1.position.column, issue_1.position.row) == (prepared_table_artifact.value[0][1])

    issue_2 = validation_result.issues[entity_code_1].errors[-1]
    assert issue_2.message == "Table contains errors"


@pytest.mark.model_business_check
def test_depended_rule__is_failed(
    document_id,
    entity_code_1,
    invalid_data_set_for_depended_rule,
    document_type: DocumentType,
    prepared_table_artifact: DocumentArtifact,
):
    error_message = uuid4().hex

    document_type.add_error_check_to_validator(
        entity_code_1,
        name=uuid4().hex,
        rule=f"check_dependency(type_code__{entity_code_1}__0, type_code__{entity_code_1}__2)",
        issue_message=error_message,
        check_optional_fields=True,
    )

    prepared_table_artifact.value[0][0] = invalid_data_set_for_depended_rule[0]
    prepared_table_artifact.value[2][0] = invalid_data_set_for_depended_rule[1]

    document_type.record_local_validation(document_id, [prepared_table_artifact])
    validation_result = document_type.derive_validation_result()

    assert not validation_result.is_valid

    issue_3 = validation_result.issues[entity_code_1].errors[-1]
    assert issue_3.message == "Table contains errors"


@pytest.mark.model_business_check
def test_depended_rule__is_valid(
    document_id,
    entity_code_1,
    valid_data_set_for_depended_rule,
    document_type: DocumentType,
    prepared_table_artifact: DocumentArtifact,
):
    error_message = uuid4().hex

    document_type.add_error_check_to_validator(
        entity_code_1,
        name=uuid4().hex,
        rule=f"check_dependency(type_code__{entity_code_1}__0, type_code__{entity_code_1}__1)",
        issue_message=error_message,
        check_optional_fields=True,
    )

    prepared_table_artifact.value[0][0] = valid_data_set_for_depended_rule[0]
    prepared_table_artifact.value[2][0] = valid_data_set_for_depended_rule[1]

    document_type.record_local_validation(document_id, [prepared_table_artifact])
    validation_result = document_type.derive_validation_result()

    assert all(not issues.has_rules_check_issues for issues in validation_result.issues.values())


@pytest.mark.model_business_check
def test_depended_rule__three_depended_columns__is_valid(
    document_id,
    entity_code_1,
    document_type: DocumentType,
    prepared_table_artifact: DocumentArtifact,
):
    error_message = uuid4().hex

    document_type.add_error_check_to_validator(
        entity_code_1,
        name=uuid4().hex,
        rule=f"check_dependency(type_code__{entity_code_1}__0, type_code__{entity_code_1}__1), type_code__{entity_code_1}__2), type_code__{entity_code_1}__3)",
        issue_message=error_message,
        check_optional_fields=True,
    )

    document_type.record_local_validation(document_id, [prepared_table_artifact])
    validation_result = document_type.derive_validation_result()

    assert validation_result.is_valid
