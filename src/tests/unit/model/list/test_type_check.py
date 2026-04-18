import pytest

from deps_high_sparrow.domain.model import DocumentArtifact, DocumentType


@pytest.mark.model_type_check
def test_table_array_validation__table_type__pass(
    document_id,
    document_type: DocumentType,
    prepared_key_value_list_artifact: DocumentArtifact,
    prepared_table_list_artifact: DocumentArtifact,
    prepared_number_list_artifact: DocumentArtifact,
    prepared_string_list_artifact: DocumentArtifact,
):
    document_type.record_local_validation(
        document_id,
        [
            prepared_key_value_list_artifact,
            prepared_table_list_artifact,
            prepared_number_list_artifact,
            prepared_string_list_artifact,
        ],
    )
    validation_result = document_type.derive_validation_result()

    assert validation_result.is_valid


@pytest.mark.model_type_check
def test_table_array_validation___table_type_fail(
    document_id,
    entity_code_2,
    document_type: DocumentType,
    prepared_table_list_artifact: DocumentArtifact,
):
    prepared_table_list_artifact.value[0][0][0] = "Not a number"
    document_type.record_local_validation(document_id, [prepared_table_list_artifact])
    validation_result = document_type.derive_validation_result()

    assert not validation_result.is_valid

    issue = validation_result.issues[entity_code_2].errors[0]

    assert "Invalid type: Field is not a number" == issue.message
    assert (0, 0) == (issue.position.column, issue.position.row)
    assert 0 == issue.position.index


@pytest.mark.model_type_check
def test_array_validation__number_type__failed(
    document_id,
    document_type: DocumentType,
    prepared_number_list_artifact: DocumentArtifact,
):
    prepared_number_list_artifact.value[0] = "Not a Number"
    document_type.record_local_validation(document_id, [prepared_number_list_artifact])
    validation_result = document_type.derive_validation_result()

    assert not validation_result.is_valid


@pytest.mark.model_type_check
def test_array_validation__no_a_list__raise_error(
    document_id,
    entity_code_2,
    document_type: DocumentType,
    prepared_table_list_artifact: DocumentArtifact,
):
    prepared_table_list_artifact.value = None
    document_type.record_local_validation(document_id, [prepared_table_list_artifact])
    validation_result = document_type.derive_validation_result()

    assert not validation_result.is_valid

    issue = validation_result.issues[entity_code_2].errors[0]

    assert "Field is required" == issue.message
