import pytest


@pytest.mark.model_pre_check
def test_all_valid(document_type, document_id, prepared_artifact_1, prepared_artifact_2):
    document_type.record_local_validation(document_id, [prepared_artifact_1, prepared_artifact_2])
    validation_result = document_type.derive_validation_result()

    assert validation_result.is_valid


@pytest.mark.model_pre_check
def test_one_required_field_is_none(document_type, document_id, entity_code_2, prepared_artifact_1):
    document_type.record_local_validation(document_id, [prepared_artifact_1])
    validation_result = document_type.derive_validation_result()

    assert not validation_result.is_valid
    assert validation_result.issues[entity_code_2].errors[0].message == "Field is required"
