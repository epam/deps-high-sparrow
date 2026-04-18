from http import HTTPStatus

import pytest

from deps_high_sparrow.constants import ENCODED_SLASH, V1_API_PREFIX
from deps_high_sparrow.domain.model import IDocumentTypeRepository


@pytest.mark.rule
def test_delete_layout__no_content(
    client,
    document_type_id,
    validator_code,
    rule_name,
    create_rule_request,
    document_type_with_string_validator,
    fake_document_type_repository: IDocumentTypeRepository,
):
    fake_document_type_repository.save(document_type_with_string_validator)

    response = client.delete(
        f"{V1_API_PREFIX}/document-types/{document_type_id}/validators/{validator_code}/rules/{rule_name}"
    )

    assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.rule
def test_delete_rule_with_slash__no_content(
    client,
    tenant_id,
    document_type_id,
    validator_code,
    rule_name_with_slash,
    document_type_with_string_validator_and_one_rule_with_slash,
    fake_document_type_repository: IDocumentTypeRepository,
):
    fake_document_type_repository.save(document_type_with_string_validator_and_one_rule_with_slash)
    encoded_rule_name = rule_name_with_slash.replace("/", ENCODED_SLASH)

    response = client.delete(
        f"{V1_API_PREFIX}/document-types/{document_type_id}/validators/{validator_code}/rules/{encoded_rule_name}"
    )

    validator = fake_document_type_repository.document_type_of_id(document_type_id, tenant_id).validators[0]

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert len(validator.rules) == 0
