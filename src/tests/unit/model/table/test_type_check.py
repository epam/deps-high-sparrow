import pytest

from deps_high_sparrow.domain.model import DocumentArtifact, DocumentType


@pytest.mark.model_type_check
def test_validation_with_valid_cells(
    document_id,
    document_type: DocumentType,
    prepared_table_artifact: DocumentArtifact,
):
    document_type.record_local_validation(document_id, [prepared_table_artifact])
    validation_result = document_type.derive_validation_result()

    assert validation_result.is_valid


@pytest.mark.model_type_check
def test_validation_with_invalid_cell(
    document_id,
    entity_code_1,
    document_type: DocumentType,
    prepared_table_artifact: DocumentArtifact,
):
    prepared_table_artifact.value[0][0] = "not a number"

    document_type.record_local_validation(document_id, [prepared_table_artifact])
    validation_result = document_type.derive_validation_result()

    assert not validation_result.is_valid

    issue = validation_result.issues[entity_code_1].errors[0]
    assert issue.message == "Invalid type: Field is not a number"
    assert (issue.position.column, issue.position.row) == (prepared_table_artifact.value[0][1])


@pytest.mark.model_type_check
def test_validation_with_invalid_optional_cell(
    document_id,
    entity_code_1,
    document_type: DocumentType,
    prepared_table_artifact: DocumentArtifact,
):
    prepared_table_artifact.value[1][0] = "not a date"

    document_type.record_local_validation(document_id, [prepared_table_artifact])
    validation_result = document_type.derive_validation_result()

    assert not validation_result.is_valid
    issue = validation_result.issues[entity_code_1].errors[0]
    assert issue.message == "Invalid type: Field is not a date or invalid date format"
    assert (issue.position.column, issue.position.row) == (prepared_table_artifact.value[1][1])


@pytest.mark.model_type_check
def test_validation_with_empty_optional_cell(
    document_id,
    empty_value,
    document_type: DocumentType,
    prepared_table_artifact: DocumentArtifact,
):
    prepared_table_artifact.value[1][0] = empty_value

    document_type.record_local_validation(document_id, [prepared_table_artifact])
    validation_result = document_type.derive_validation_result()

    assert validation_result.is_valid
