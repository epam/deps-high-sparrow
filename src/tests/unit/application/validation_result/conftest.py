from copy import deepcopy
from random import randint
from typing import Any

import pytest
import requests_mock

from deps_high_sparrow.domain.model import (
    DocumentType,
    DocumentTypeFactory,
    Severity,
    ValidationResult,
)
from deps_high_sparrow.infrastructure.proxies.extraction.value_unit import (
    ExtractedDataValueUnit,
)
from tests.data.extracted_data import with_string_field

FIRST_ELEMENT = 0


@pytest.fixture
def document_id() -> str:
    return str(randint(1, 9999))


@pytest.fixture
def edata_with_string_field(document_id) -> dict[str, Any]:
    edata = deepcopy(with_string_field)
    edata["documentId"] = document_id

    return edata


@pytest.fixture
def get_edata_request_mock(document_id, extraction_proxy, edata_with_string_field):
    with requests_mock.Mocker() as m:
        m.register_uri(
            url=f"{extraction_proxy._base_url}{extraction_proxy.v2_url_suffix}/extracted-data/{document_id}",
            method="GET",
            json=edata_with_string_field,
        )
        yield m


@pytest.fixture
def document_type_with_field_validators(
    document_type_id,
    tenant_id,
    entity_code_1,
    entity_code_2,
    entity_code_3,
) -> DocumentType:
    document_type = DocumentTypeFactory.create(
        id_=document_type_id,
        tenant_id=tenant_id,
    )
    document_type.add_string_validator(entity_code_1).with_description().is_required().build()
    document_type.add_string_validator(entity_code_2).with_description().is_required().build()
    document_type.add_string_validator(entity_code_3).with_description().build()
    return document_type


@pytest.fixture
def document_type_with_cross_field_rules(
    document_type_with_field_validators,
    entity_code_1,
    entity_code_2,
) -> DocumentType:
    document_type_with_field_validators.add_cross_field_validator(
        name="field1_equals_field2",
        description="Field1 must equal Field2",
        rule=f"F{entity_code_1} == F{entity_code_2}",
        severity=Severity.ERROR,
        validated_fields=[entity_code_1],
        issue_message=f"Field1 must match ${{{entity_code_2}}}",
        dependent_fields=[entity_code_2],
    )
    return document_type_with_field_validators


@pytest.fixture
def value_units_two_fields(entity_code_1, entity_code_2):
    return [
        ExtractedDataValueUnit(code=entity_code_1, value="value1"),
        ExtractedDataValueUnit(code=entity_code_2, value="value2"),
    ]


@pytest.fixture
def value_units_field1_only(entity_code_1):
    return [
        ExtractedDataValueUnit(code=entity_code_1, value="some_value"),
    ]


@pytest.fixture
def value_units_field3_only(entity_code_3):
    return [
        ExtractedDataValueUnit(code=entity_code_3, value="some_value"),
    ]


@pytest.fixture
def existing_validation_result(document_id, tenant_id) -> ValidationResult:
    return ValidationResult(id=document_id, tenant_id=tenant_id)


@pytest.fixture
def saved_document_type_with_field_validators(
    fake_document_type_repository,
    document_type_with_field_validators,
) -> DocumentType:
    fake_document_type_repository.save(document_type_with_field_validators)
    return document_type_with_field_validators


@pytest.fixture
def saved_document_type_with_cross_field_rules(
    fake_document_type_repository,
    document_type_with_cross_field_rules,
) -> DocumentType:
    fake_document_type_repository.save(document_type_with_cross_field_rules)
    return document_type_with_cross_field_rules
