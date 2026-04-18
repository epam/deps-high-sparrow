from http import HTTPStatus

import pytest

from deps_high_sparrow.constants import V1_API_PREFIX
from deps_high_sparrow.domain.model import IDocumentTypeRepository


@pytest.mark.rule
def test_create_rule__success(
    client,
    document_type_id,
    validator_code,
    tenant_id,
    create_rule_request,
    document_type_with_string_validator,
    fake_document_type_repository: IDocumentTypeRepository,
):
    fake_document_type_repository.save(document_type_with_string_validator)
    response = client.post(
        f"{V1_API_PREFIX}/document-types/{document_type_id}/validators/{validator_code}/rules",
        data=create_rule_request.model_dump_json(),
    )
    created_rule = response.json()

    assert response.status_code == HTTPStatus.CREATED
    assert created_rule["name"] == create_rule_request.name
    assert created_rule["severity"] == create_rule_request.severity.value
    assert created_rule["rule"] == create_rule_request.rule
    assert created_rule["issueMessage"] == create_rule_request.issue_message
    assert created_rule["description"] == create_rule_request.description
    assert created_rule["needWarningEvenIfOptional"] == create_rule_request.need_warning_even_if_optional
    assert created_rule["forEach"] == create_rule_request.for_each
    assert created_rule["forAny"] == create_rule_request.for_any
    assert created_rule["checkOptionalFields"] == create_rule_request.check_optional_fields


@pytest.mark.rule
def test_create_rule__document_type_not_found(
    client,
    validator_code,
    create_rule_request,
):
    not_existed_document_type_id = "not_existed_document_type_id"
    response = client.post(
        f"{V1_API_PREFIX}/document-types/{not_existed_document_type_id}/validators/{validator_code}/rules",
        data=create_rule_request.model_dump_json(),
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.rule
def test_create_rule__validator_not_found(
    client,
    document_type_id,
    create_rule_request,
    document_type,
    fake_document_type_repository: IDocumentTypeRepository,
):
    fake_document_type_repository.save(document_type)
    not_existed_validator_code = "not_existed_validator_code"
    response = client.post(
        f"{V1_API_PREFIX}/document-types/{document_type_id}/validators/{not_existed_validator_code}/rules",
        data=create_rule_request.model_dump_json(),
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.rule
def test_create_rule__rule_already_exists(
    client,
    document_type_id,
    validator_code,
    tenant_id,
    create_rule_request,
    document_type_with_string_validator_and_one_rule,
    fake_document_type_repository: IDocumentTypeRepository,
):
    fake_document_type_repository.save(document_type_with_string_validator_and_one_rule)
    response = client.post(
        f"{V1_API_PREFIX}/document-types/{document_type_id}/validators/{validator_code}/rules",
        data=create_rule_request.model_dump_json(),
    )

    assert response.status_code == HTTPStatus.CONFLICT
