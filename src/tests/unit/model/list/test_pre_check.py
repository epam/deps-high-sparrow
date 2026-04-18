import pytest

from deps_high_sparrow.domain.model import DocumentArtifact, DocumentType


@pytest.mark.model_pre_check
def test_required_array__is_valid(
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


@pytest.mark.model_pre_check
def test_required_array_of_dicts__item_is_none(
    document_id,
    entity_code_1,
    document_type: DocumentType,
    prepared_key_value_list_artifact: DocumentArtifact,
):
    expected_messages = {
        "Array contains errors",
        "Key is required",
        "Value is required",
    }

    prepared_key_value_list_artifact.value[0] = (None, None)

    document_type.record_local_validation(document_id, [prepared_key_value_list_artifact])
    validation_result = document_type.derive_validation_result()

    assert not validation_result.is_valid
    assert expected_messages == {issue.message for issue in validation_result.issues[entity_code_1].errors}


@pytest.mark.model_pre_check
def test_list_of_tables__required_cell_is_none(
    document_id,
    entity_code_2,
    document_type: DocumentType,
    prepared_table_list_artifact: DocumentArtifact,
):
    prepared_table_list_artifact.value[0][0][0] = None

    document_type.record_local_validation(document_id, [prepared_table_list_artifact])
    validation_result = document_type.derive_validation_result()

    assert not validation_result.is_valid
    issue = validation_result.issues[entity_code_2].errors[0]
    assert "Column is required" == issue.message
    assert (0, 0) == (issue.position.column, issue.position.row)
    assert 0 == issue.position.index
