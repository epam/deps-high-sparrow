from uuid import uuid4

import pytest

from deps_high_sparrow.domain.events import BusinessRuleViolated
from deps_high_sparrow.domain.model.document_type.validator.validator import (
    BusinessRulesValidationService,
)


@pytest.mark.model_type_check
def test_all_valid(document_type, document_id, entity_code_1, prepared_artifact_1, prepared_artifact_2):
    document_type.add_warning_check_to_validator(
        entity_code_1,
        name=uuid4().hex,
        rule=f"type_code__{entity_code_1} == 1",
        issue_message="Warning",
    )

    document_type.record_local_validation(document_id, [prepared_artifact_1, prepared_artifact_2])
    validation_result = document_type.derive_validation_result()

    assert validation_result.is_valid


@pytest.mark.model_type_check
def test_is_not_valid(document_type, document_id, entity_code_1, prepared_artifact_1, prepared_artifact_2):
    error_message = uuid4().hex
    events = [BusinessRuleViolated(document_id=document_id, field_code=entity_code_1, message=error_message)]

    document_type.add_error_check_to_validator(
        entity_code_1,
        name=uuid4().hex,
        rule=f"type_code__{entity_code_1} == 55",
        issue_message=error_message,
    )

    document_type.record_local_validation(document_id, [prepared_artifact_1, prepared_artifact_2])
    validation_result = document_type.derive_validation_result()

    assert not validation_result.is_valid
    assert validation_result.issues[entity_code_1].errors[0].message == error_message
    assert validation_result.events == events


@pytest.mark.model_type_check
def test_warning_but_valid(document_type, document_id, entity_code_1, prepared_artifact_1, prepared_artifact_2):
    error_message = uuid4().hex

    document_type.add_warning_check_to_validator(
        entity_code_1,
        name=uuid4().hex,
        rule=f"type_code__{entity_code_1} == 55",
        issue_message=error_message,
    )

    document_type.record_local_validation(document_id, [prepared_artifact_1, prepared_artifact_2])
    validation_result = document_type.derive_validation_result()

    assert validation_result.is_valid
    assert validation_result.issues[entity_code_1].warnings[0].message == error_message


@pytest.mark.model_type_check
def test_2_rules_is_not_valid(document_type, document_id, entity_code_1, prepared_artifact_1, prepared_artifact_2):
    error_message = uuid4().hex

    document_type.add_error_check_to_validator(
        entity_code_1,
        name=uuid4().hex,
        rule=f"type_code__{entity_code_1} == 55",
        issue_message=error_message,
    )

    document_type.add_warning_check_to_validator(
        entity_code_1,
        name=uuid4().hex,
        rule=f"type_code__{entity_code_1} == 55",
        issue_message=error_message,
    )

    document_type.record_local_validation(document_id, [prepared_artifact_1, prepared_artifact_2])
    validation_result = document_type.derive_validation_result()

    assert not validation_result.is_valid
    assert validation_result.issues[entity_code_1].errors[0].message == error_message
    assert validation_result.issues[entity_code_1].warnings[0].message == error_message


@pytest.mark.model_type_check
def test_parser_raises_exception__system_error_message(
    document_type, document_id, entity_code_1, prepared_artifact_1, prepared_artifact_2
):
    document_type.add_error_check_to_validator(
        entity_code_1,
        name=uuid4().hex,
        rule=f"UNPARSABLE",
        issue_message=uuid4().hex,
    )

    document_type.record_local_validation(document_id, [prepared_artifact_1, prepared_artifact_2])
    validation_result = document_type.derive_validation_result()

    assert not validation_result.is_valid
    assert (
        validation_result.issues[entity_code_1].errors[0].message == BusinessRulesValidationService.SYSTEM_ERROR_MESSAGE
    )
