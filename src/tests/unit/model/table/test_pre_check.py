import pytest

from deps_high_sparrow.domain.model import DocumentArtifact, DocumentType
from deps_high_sparrow.domain.model.document_type.validator.validation.services import (
    RequiredFieldsPreCheckService,
)


@pytest.mark.model_pre_check
def test_all_table_cell_valid(
    document_id,
    document_type: DocumentType,
    prepared_table_artifact: DocumentArtifact,
):
    document_type.record_local_validation(document_id, [prepared_table_artifact])
    validation_result = document_type.derive_validation_result()

    assert validation_result.is_valid


@pytest.mark.model_pre_check
def test_optional_cell_is_none(
    document_id,
    empty_value,
    document_type: DocumentType,
    prepared_table_artifact: DocumentArtifact,
):
    prepared_table_artifact.value[1][0] = empty_value

    document_type.record_local_validation(document_id, [prepared_table_artifact])
    validation_result = document_type.derive_validation_result()

    assert validation_result.is_valid


@pytest.mark.model_pre_check
def test_required_cell_is_none(
    document_id,
    entity_code_1,
    empty_value,
    document_type: DocumentType,
    prepared_table_artifact: DocumentArtifact,
):
    prepared_table_artifact.value[0][0] = empty_value

    document_type.record_local_validation(document_id, [prepared_table_artifact])
    validation_result = document_type.derive_validation_result()

    assert not validation_result.is_valid
    issue = validation_result.issues[entity_code_1].errors[0]
    assert issue.message == "Column is required"
    assert (issue.position.column, issue.position.row) == (prepared_table_artifact.value[0][1])


@pytest.mark.model_pre_check
def test_required_table_is_empty(
    document_id,
    entity_code_1,
    document_type: DocumentType,
    prepared_table_artifact: DocumentArtifact,
):
    prepared_table_artifact.value = []

    document_type.record_local_validation(document_id, [prepared_table_artifact])
    validation_result = document_type.derive_validation_result()

    assert not validation_result.is_valid

    issue = validation_result.issues[entity_code_1].errors[0]
    assert issue.message == "Field is required"


@pytest.mark.model_pre_check
def test_required_table_is_not_provided(
    document_id,
    entity_code_1,
    document_type: DocumentType,
):
    document_type.record_local_validation(document_id, [])
    validation_result = document_type.derive_validation_result()

    assert not validation_result.is_valid

    issue = validation_result.issues[entity_code_1].errors[0]
    assert issue.message == "Field is required"


@pytest.mark.model_pre_check
def test_required_table_is_none(
    document_id,
    entity_code_1,
    document_type: DocumentType,
    prepared_table_artifact: DocumentArtifact,
):
    prepared_table_artifact.value = None

    document_type.record_local_validation(document_id, [prepared_table_artifact])
    validation_result = document_type.derive_validation_result()

    assert not validation_result.is_valid

    issue = validation_result.issues[entity_code_1].errors[0]
    assert issue.message == "Field is required"


@pytest.mark.model_pre_check
def test_cell_out_of_bounds(
    document_id: str,
    entity_code_1: str,
    document_type: DocumentType,
    prepared_table_artifact: DocumentArtifact,
):
    prepared_table_artifact.value.append(("1", (3, 0)))

    document_type.record_local_validation(document_id, [prepared_table_artifact])
    validation_result = document_type.derive_validation_result()

    assert not validation_result.is_valid

    issue = validation_result.issues[entity_code_1].errors[0]
    assert issue.message == RequiredFieldsPreCheckService.CELLS_OUT_OF_BOUNDS
