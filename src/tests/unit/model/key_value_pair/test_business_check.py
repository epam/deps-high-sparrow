from uuid import uuid4

import pytest

from deps_high_sparrow.domain.model import DocumentArtifact, DocumentType


@pytest.mark.model_business_check
def test_is_valid(
    document_id,
    entity_code_1,
    document_type: DocumentType,
    prepared_key_value_artifact_1: DocumentArtifact,
):
    error_message = uuid4().hex

    document_type.add_error_check_to_validator(
        entity_code_1,
        name=uuid4().hex,
        rule=f"type_code__{entity_code_1}__0 == 'val'",
        issue_message=error_message,
    )
    document_type.record_local_validation(document_id, [prepared_key_value_artifact_1])
    validation_result = document_type.derive_validation_result()

    assert validation_result.is_valid


@pytest.mark.model_business_check
def test_warning_is_valid(
    document_id,
    entity_code_1,
    document_type: DocumentType,
    prepared_key_value_artifact_1: DocumentArtifact,
):
    error_message = uuid4().hex

    document_type.add_warning_check_to_validator(
        entity_code_1,
        name=uuid4().hex,
        rule=f"type_code__{entity_code_1}__0 != 'val'",
        issue_message=error_message,
    )
    document_type.record_local_validation(document_id, [prepared_key_value_artifact_1])
    validation_result = document_type.derive_validation_result()

    assert validation_result.is_valid

    issue = validation_result.issues[entity_code_1].warnings[0]
    assert "key" == issue.position.kv_id
    assert error_message == issue.message


@pytest.mark.model_business_check
def test_warning_is_not_valid(
    document_id,
    entity_code_1,
    document_type: DocumentType,
    prepared_key_value_artifact_1: DocumentArtifact,
):
    error_message = uuid4().hex

    document_type.add_error_check_to_validator(
        entity_code_1,
        name=uuid4().hex,
        rule=f"type_code__{entity_code_1}__0 != 'val'",
        issue_message=error_message,
    )
    document_type.record_local_validation(document_id, [prepared_key_value_artifact_1])
    validation_result = document_type.derive_validation_result()

    assert not validation_result.is_valid

    issue = validation_result.issues[entity_code_1].errors[0]
    assert "key" == issue.position.kv_id
    assert error_message == issue.message
