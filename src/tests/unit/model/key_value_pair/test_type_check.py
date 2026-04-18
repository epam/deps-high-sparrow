import pytest

from deps_high_sparrow.domain.model import DocumentArtifact, DocumentType


@pytest.mark.model_type_check
def test_correct_value__pass(
    document_id,
    document_type: DocumentType,
    prepared_key_value_artifact_1: DocumentArtifact,
):
    document_type.record_local_validation(document_id, [prepared_key_value_artifact_1])
    validation_result = document_type.derive_validation_result()

    assert validation_result.is_valid
