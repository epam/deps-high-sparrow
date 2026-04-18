from http import HTTPStatus
from typing import Any
from uuid import uuid4

import pytest

from deps_high_sparrow.constants import V1_API_PREFIX
from deps_high_sparrow.domain import DocumentType, NotFoundError, Severity
from deps_high_sparrow.domain.model import IDocumentTypeRepository


@pytest.mark.document_type
def test_find_document_type_with_key_value_validator__success(
    client,
    document_type_id,
    tenant_id,
    document_type_with_key_value_validator,
    fake_document_type_repository: IDocumentTypeRepository,
):
    fake_document_type_repository.save(document_type_with_key_value_validator)
    response = client.get(f"{V1_API_PREFIX}/document-types/{document_type_id}")
    document_type = response.json()

    assert response.status_code == HTTPStatus.OK
    assert document_type["id"] == document_type_with_key_value_validator.id()

    expected_validators = document_type_with_key_value_validator.validators

    for real_validator, expected_validator in zip(document_type["validators"], expected_validators):
        assert real_validator["code"] == expected_validator.code.value
        assert real_validator["isRequired"] == expected_validator.is_required

        validator_type = real_validator["type"]
        assert validator_type["type"] == expected_validator.type_.type.value

        if expected_validator.type_.description is not None:
            assert validator_type["description"]["keyType"] == expected_validator.type_.description.key_type
            assert validator_type["description"]["valueType"] == expected_validator.type_.description.value_type


@pytest.mark.document_type
def test_find_document_type_with_list_of_key_value_validators__success(
    client,
    document_type_id,
    tenant_id,
    document_type_with_list_of_key_value_validators,
    fake_document_type_repository: IDocumentTypeRepository,
):
    fake_document_type_repository.save(document_type_with_list_of_key_value_validators)
    response = client.get(f"{V1_API_PREFIX}/document-types/{document_type_id}")
    document_type = response.json()

    assert response.status_code == HTTPStatus.OK
    assert document_type["id"] == document_type_with_list_of_key_value_validators.id()

    expected_validators = document_type_with_list_of_key_value_validators.validators

    for real_validator, expected_validator in zip(document_type["validators"], expected_validators):
        assert real_validator["code"] == expected_validator.code.value
        assert real_validator["isRequired"] == expected_validator.is_required

        validator_type = real_validator["type"]
        assert validator_type["type"] == expected_validator.type_.type.value

        if expected_validator.type_.description is not None:
            assert validator_type["description"]["itemType"] == expected_validator.type_.description.item_type
            assert (
                validator_type["description"]["meta"]["keyType"] == expected_validator.type_.description.meta.key_type
            )
            assert (
                validator_type["description"]["meta"]["valueType"]
                == expected_validator.type_.description.meta.value_type
            )


@pytest.mark.document_type
def test_find_document_type_with_string_validator__success(
    client,
    document_type_id,
    tenant_id,
    document_type_with_string_validator_and_one_rule,
    fake_document_type_repository: IDocumentTypeRepository,
):
    fake_document_type_repository.save(document_type_with_string_validator_and_one_rule)
    response = client.get(f"{V1_API_PREFIX}/document-types/{document_type_id}")
    document_type = response.json()

    assert response.status_code == HTTPStatus.OK
    assert document_type["id"] == document_type_with_string_validator_and_one_rule.id()

    expected_validators = document_type_with_string_validator_and_one_rule.validators

    for real_validator, expected_validator in zip(document_type["validators"], expected_validators):
        assert real_validator["code"] == expected_validator.code.value
        assert real_validator["isRequired"] == expected_validator.is_required

        validator_type = real_validator["type"]
        assert validator_type["type"] == expected_validator.type_.type.value

        for real_rule, expected_rule in zip(real_validator["rules"], expected_validator.rules.values()):
            assert real_rule["name"] == expected_rule.name
            assert real_rule["severity"] == expected_rule.severity.value
            assert real_rule["rule"] == expected_rule.rule
            assert real_rule["issueMessage"] == expected_rule.issue_message


@pytest.mark.document_type
def test_find_document_type_with_table_validator__success(
    client,
    document_type_id,
    tenant_id,
    document_type_with_table_validator,
    fake_document_type_repository: IDocumentTypeRepository,
):
    fake_document_type_repository.save(document_type_with_table_validator)
    response = client.get(f"{V1_API_PREFIX}/document-types/{document_type_id}")
    document_type = response.json()

    assert response.status_code == HTTPStatus.OK
    assert document_type["id"] == document_type_with_table_validator.id()

    expected_validators = document_type_with_table_validator.validators

    for real_validator, expected_validator in zip(document_type["validators"], expected_validators):
        assert real_validator["code"] == expected_validator.code.value
        assert real_validator["isRequired"] == expected_validator.is_required

        validator_type = real_validator["type"]
        assert validator_type["type"] == expected_validator.type_.type.value

        if expected_validator.type_.description is not None:
            real_columns = validator_type["description"]["columns"]
            assert isinstance(real_columns, list)

            for real_column, expected_column in zip(real_columns, expected_validator.type_.description.columns):
                assert real_column["index"] == expected_column.index
                assert real_column["isRequired"] == expected_column.is_required
                assert real_column["itemType"] == expected_column.item_type


@pytest.mark.document_type
def test_find_document_type__document_type_not_found(
    client,
    document_type_id,
    tenant_id,
):
    not_existed_document_type_id = "not_existed_document_type_id"
    response = client.get(f"{V1_API_PREFIX}/document-types/{not_existed_document_type_id}")

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.document_type
def test_attach_validator__success(
    client,
    fake_document_type_repository: IDocumentTypeRepository,
    document_type,
    document_type_id,
    tenant_id,
    external_validator_name,
    external_validator_url,
    external_validator,
):
    fake_document_type_repository.save(document_type)

    payload = {"name": external_validator_name, "url": external_validator_url}

    response = client.post(url=f"{V1_API_PREFIX}/document-types/{document_type_id}/external-validators", json=payload)

    assert response.status_code == HTTPStatus.CREATED
    saved_document_type = fake_document_type_repository.document_type_of_id(
        document_type_id=document_type_id, tenant_id=tenant_id
    )
    assert len(saved_document_type.external_validators) == 1
    assert saved_document_type.external_validators[0] == external_validator


@pytest.mark.document_type
def test_remove_validator__success(
    client,
    fake_document_type_repository: IDocumentTypeRepository,
    document_type_with_external_validator,
    document_type_id,
    tenant_id,
    external_validator_name,
):
    fake_document_type_repository.save(document_type_with_external_validator)

    response = client.delete(
        url=f"{V1_API_PREFIX}/document-types/{document_type_id}/external-validators/{external_validator_name}"
    )

    assert response.status_code == HTTPStatus.NO_CONTENT
    saved_document_type = fake_document_type_repository.document_type_of_id(
        document_type_id=document_type_id, tenant_id=tenant_id
    )
    assert len(saved_document_type.external_validators) == 0


@pytest.mark.document_type
def test_add_cross_field_validator__valid_request__created(
    client,
    fake_document_type_repository: IDocumentTypeRepository,
    document_type_with_validators,
    document_type_id,
    tenant_id,
    cross_field_validator_name,
    cross_field_validator_description,
    cross_field_validator_rule,
    cross_field_validated_fields,
    cross_field_issue_message_text,
    cross_field_dependent_fields,
):
    validated_field_ids = [field.value for field in cross_field_validated_fields]
    dependent_field_ids = [field.value for field in cross_field_dependent_fields]

    fake_document_type_repository.save(document_type_with_validators)

    payload = {
        "name": cross_field_validator_name,
        "description": cross_field_validator_description,
        "rule": cross_field_validator_rule,
        "severity": "error",
        "validatedFields": validated_field_ids,
        "issueMessage": cross_field_issue_message_text,
        "dependentFields": dependent_field_ids,
        "forEach": False,
        "forAny": False,
    }

    response = client.post(
        url=f"{V1_API_PREFIX}/document-types/{document_type_id}/cross-field-validators",
        json=payload,
    )

    assert response.status_code == HTTPStatus.CREATED

    response_data = response.json()
    assert isinstance(response_data, dict)
    assert "id" in response_data
    validator_id = response_data["id"]
    assert isinstance(validator_id, str)
    assert validator_id

    saved_document_type = fake_document_type_repository.document_type_of_id(
        document_type_id=document_type_id, tenant_id=tenant_id
    )
    assert len(saved_document_type.cross_field_validators) == 1
    validator = saved_document_type.cross_field_validators[0]
    assert validator.id() == validator_id
    assert validator.name == cross_field_validator_name
    assert validator.description == cross_field_validator_description
    assert validator.rule == cross_field_validator_rule
    assert validator.severity == Severity.ERROR


@pytest.mark.document_type
def test_add_cross_field_validator__document_type_not_found__not_found(
    client,
    document_type_id,
    cross_field_validator_name,
    cross_field_validator_description,
    cross_field_validator_rule,
    cross_field_validated_fields,
    cross_field_issue_message_text,
    cross_field_dependent_fields,
):
    payload = {
        "name": cross_field_validator_name,
        "description": cross_field_validator_description,
        "rule": cross_field_validator_rule,
        "severity": "error",
        "validatedFields": [field.value for field in cross_field_validated_fields],
        "issueMessage": cross_field_issue_message_text,
        "dependentFields": [field.value for field in cross_field_dependent_fields],
    }

    response = client.post(
        url=f"{V1_API_PREFIX}/document-types/{document_type_id}/cross-field-validators",
        json=payload,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.document_type
def test_update_cross_field_validator__success(
    client,
    document_type_id,
    tenant_id,
    fake_document_type_repository: IDocumentTypeRepository,
    document_type_with_all_validators,
):
    document_type, cross_field_validator_id = document_type_with_all_validators
    fake_document_type_repository.save(document_type)

    expected_name = "new_validator_name"
    expected_description = "new_description"
    expected_rule = "Ffield1 > 0"
    expected_severity = Severity.WARNING
    expected_fields: list[Any] = ["field1"]
    expected_issue_message = "newissuemessage ${field1}"

    payload = {
        "name": expected_name,
        "description": expected_description,
        "rule": expected_rule,
        "severity": expected_severity.value,
        "validatedFields": expected_fields,
        "issueMessage": expected_issue_message,
        "dependentFields": [],
    }

    response = client.patch(
        url=f"{V1_API_PREFIX}/document-types/{document_type_id}/cross-field-validators/{cross_field_validator_id}",
        json=payload,
    )

    assert response.status_code == HTTPStatus.OK

    saved_document_type = fake_document_type_repository.document_type_of_id(
        document_type_id=document_type_id, tenant_id=tenant_id
    )
    validator = saved_document_type.cross_field_validators[0]

    assert validator.id() == cross_field_validator_id
    assert validator.name == expected_name
    assert validator.description == expected_description
    assert validator.rule == expected_rule
    assert validator.severity == expected_severity

    validated_field_values = [field.value for field in validator.validated_fields]
    assert validated_field_values == expected_fields

    assert validator.issue_message.message == expected_issue_message

    dependent_field_values = [field.value for field in validator.issue_message.dependent_fields]
    assert dependent_field_values == []


@pytest.mark.document_type
def test_update_cross_field_validator_name__success(
    client,
    document_type_id,
    tenant_id,
    fake_document_type_repository: IDocumentTypeRepository,
    document_type_with_all_validators,
):
    document_type, cross_field_validator_id = document_type_with_all_validators
    fake_document_type_repository.save(document_type)

    pre_test_document_type = fake_document_type_repository.document_type_of_id(
        document_type_id=document_type_id, tenant_id=tenant_id
    )
    pre_test_validator = pre_test_document_type.cross_field_validators[0]

    expected_name = "new_validator_name"
    payload = {"name": expected_name}

    response = client.patch(
        url=f"{V1_API_PREFIX}/document-types/{document_type_id}/cross-field-validators/{cross_field_validator_id}",
        json=payload,
    )

    assert response.status_code == HTTPStatus.OK

    saved_document_type = fake_document_type_repository.document_type_of_id(
        document_type_id=document_type_id, tenant_id=tenant_id
    )
    validator = saved_document_type.cross_field_validators[0]

    assert validator.id() == cross_field_validator_id
    assert validator.name == expected_name
    assert validator.description == pre_test_validator.description
    assert validator.rule == pre_test_validator.rule
    assert validator.severity == pre_test_validator.severity
    assert validator.validated_fields == pre_test_validator.validated_fields
    assert validator.issue_message.message == pre_test_validator.issue_message.message
    assert validator.issue_message.dependent_fields == pre_test_validator.issue_message.dependent_fields


@pytest.mark.document_type
def test_update_cross_field_validator_with_duplicate_name__fails(
    client,
    document_type_id,
    tenant_id,
    fake_document_type_repository: IDocumentTypeRepository,
    document_type_with_all_validators,
):
    document_type, first_validator_id = document_type_with_all_validators

    second_validator_id = document_type.add_cross_field_validator(
        name="second_validator_name",
        description="Second validator description",
        rule="Ffield3 == Ffield4",
        severity=Severity.WARNING,
        validated_fields=["field3", "field4"],
        issue_message="Fields ${field3} and ${field4} should match",
        dependent_fields=["field3", "field4"],
    )

    fake_document_type_repository.save(document_type)

    pre_test_document_type = fake_document_type_repository.document_type_of_id(
        document_type_id=document_type_id, tenant_id=tenant_id
    )
    first_validator = next(v for v in pre_test_document_type.cross_field_validators if v.id() == first_validator_id)
    existing_name = first_validator.name

    payload = {"name": existing_name}

    response = client.patch(
        url=f"{V1_API_PREFIX}/document-types/{document_type_id}/cross-field-validators/{second_validator_id}",
        json=payload,
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST

    response_json = response.json()
    assert response_json["code"] == "cross_field_validator_already_exists_error"
    assert "already exists" in response_json["message"]
    assert existing_name in response_json["message"]

    saved_document_type = fake_document_type_repository.document_type_of_id(
        document_type_id=document_type_id, tenant_id=tenant_id
    )
    second_validator = next(v for v in saved_document_type.cross_field_validators if v.id() == second_validator_id)

    assert second_validator.name == "second_validator_name"


@pytest.mark.document_type
def test_delete_cross_field_validator__success(
    client,
    fake_document_type_repository: IDocumentTypeRepository,
    document_type_with_cross_field_validator,
    document_type_id,
    tenant_id,
    cross_field_validator_id,
):
    fake_document_type_repository.save(document_type_with_cross_field_validator)

    response = client.delete(
        url=f"{V1_API_PREFIX}/document-types/{document_type_id}/cross-field-validators/{cross_field_validator_id}"
    )

    assert response.status_code == HTTPStatus.NO_CONTENT

    assert not response.content

    saved_document_type = fake_document_type_repository.document_type_of_id(
        document_type_id=document_type_id, tenant_id=tenant_id
    )
    assert cross_field_validator_id not in saved_document_type._cross_field_validators


@pytest.mark.document_type
def test_delete_cross_field_validator__invalid_document_id(
    client,
):
    invalid_document_id = "non-existent-document-id"
    validator_id = "some-validator-id"

    response = client.delete(
        url=f"{V1_API_PREFIX}/document-types/{invalid_document_id}/cross-field-validators/{validator_id}"
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.document_type
def test_delete_cross_field_validator__invalid_validator_id(
    client,
    fake_document_type_repository: IDocumentTypeRepository,
    document_type_with_cross_field_validator,
    document_type_id,
    tenant_id,
):
    fake_document_type_repository.save(document_type_with_cross_field_validator)

    initial_validators_count = len(document_type_with_cross_field_validator._cross_field_validators)

    invalid_validator_id = "non-existent-validator-id"

    response = client.delete(
        url=f"{V1_API_PREFIX}/document-types/{document_type_id}/cross-field-validators/{invalid_validator_id}"
    )

    assert response.status_code == HTTPStatus.NO_CONTENT

    saved_document_type = fake_document_type_repository.document_type_of_id(
        document_type_id=document_type_id, tenant_id=tenant_id
    )
    assert len(saved_document_type._cross_field_validators) == initial_validators_count


@pytest.mark.document_type
def test_get_all_validators__ok(
    client,
    fake_document_type_repository: IDocumentTypeRepository,
    document_type_with_every_validator: DocumentType,
    document_type_id: str,
    tenant_id: str,
):
    fake_document_type_repository.save(document_type_with_every_validator)

    response = client.get(url=f"{V1_API_PREFIX}/document-types/{document_type_id}/validators")

    assert response.status_code == HTTPStatus.OK

    validators = response.json()

    assert len(validators["validators"]) == 1
    assert validators["validators"][0]["code"] == document_type_with_every_validator.validators[0].code()

    assert len(validators["crossFieldValidators"]) == 1
    assert (
        validators["crossFieldValidators"][0]["id"] == document_type_with_every_validator.cross_field_validators[0].id()
    )

    assert len(validators["externalValidators"]) == 1
    assert validators["externalValidators"][0]["name"] == document_type_with_every_validator.external_validators[0].name


@pytest.mark.document_type
def test_validate_field__ok(
    client,
    fake_document_type_repository,
    fake_extraction_proxy,
    document_type_id,
    tenant_id,
    validator_code,
    value_units_for_validator,
):
    document_type = DocumentType(id_=document_type_id, tenant_id=tenant_id)
    document_type.add_string_validator(code=validator_code).with_description().is_required().build()
    fake_document_type_repository.save(document_type)

    document_id = uuid4().hex
    fake_extraction_proxy.set_field_value_units(value_units_for_validator)

    response = client.post(
        url=f"{V1_API_PREFIX}/document-types/{document_type_id}/validators/{validator_code}/validate",
        json={"documentId": document_id},
    )

    assert response.status_code == HTTPStatus.OK

    body = response.json()
    assert "isValid" in body
    assert "detail" in body
    assert len(body["detail"]) == 1
    assert body["detail"][0]["fieldCode"] == validator_code


@pytest.mark.document_type
def test_validate_field__document_type_not_found__returns_404(
    client,
    document_type_id,
):
    response = client.post(
        url=f"{V1_API_PREFIX}/document-types/{document_type_id}/validators/any_code/validate",
        json={"documentId": uuid4().hex},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.document_type
def test_validate_field__missing_document_id__returns_422(
    client,
    document_type_id,
):
    response = client.post(
        url=f"{V1_API_PREFIX}/document-types/{document_type_id}/validators/any_code/validate",
        json={},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
