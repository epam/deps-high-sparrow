import pytest

from deps_high_sparrow.domain.model import DocumentArtifact, DocumentType


@pytest.mark.model_pre_check
def test_required_dict_values_are_set(
    document_id,
    document_type: DocumentType,
    prepared_key_value_artifact_1: DocumentArtifact,
    prepared_key_value_artifact_2: DocumentArtifact,
):
    document_type.record_local_validation(document_id, [prepared_key_value_artifact_1])
    validation_result = document_type.derive_validation_result()

    assert validation_result.is_valid


@pytest.mark.model_pre_check
def test_required_dict_not_given(
    document_id,
    entity_code_1,
    document_type: DocumentType,
):
    document_type.record_local_validation(document_id, [])
    validation_result = document_type.derive_validation_result()

    assert not validation_result.is_valid
    assert "Field is required" == validation_result.issues[entity_code_1].errors[0].message


@pytest.mark.model_pre_check
def test_required_dict_values_are_none(
    document_id,
    entity_code_1,
    document_type: DocumentType,
    prepared_key_value_artifact_1: DocumentArtifact,
):
    expected_messages = {"Key is required", "Value is required"}

    prepared_key_value_artifact_1.value = (None, None)

    document_type.record_local_validation(document_id, [prepared_key_value_artifact_1])
    validation_result = document_type.derive_validation_result()

    assert not validation_result.is_valid
    assert expected_messages == {issue.message for issue in validation_result.issues[entity_code_1].errors}


@pytest.mark.model_pre_check
def test_optional_dict_values_are_none(
    document_id,
    document_type: DocumentType,
    prepared_key_value_artifact_1: DocumentArtifact,
    prepared_key_value_artifact_2: DocumentArtifact,
):
    prepared_key_value_artifact_2.value = (None, None)

    document_type.record_local_validation(document_id, [prepared_key_value_artifact_1, prepared_key_value_artifact_2])
    validation_result = document_type.derive_validation_result()

    assert validation_result.is_valid
