from random import choice
from uuid import uuid4

import pytest
from faker import Faker

from deps_high_sparrow.domain import OperandType, Validator, ValidatorType
from deps_high_sparrow.domain.model import DocumentType, Severity

fake = Faker()


@pytest.fixture
def document_type_repository(repositories):
    return repositories.document_type()


@pytest.fixture
def validator_code() -> str:
    return uuid4().hex


@pytest.fixture
def document_type(document_type_id, tenant_id):
    return DocumentType(
        id_=document_type_id,
        tenant_id=tenant_id,
    )


@pytest.fixture
def document_type_with_string_validator(document_type, validator_code) -> DocumentType:
    document_type.add_string_validator(code=validator_code).is_required().build()
    return document_type


@pytest.fixture
def document_type_with_string_validator_and_one_rule(
    document_type_with_string_validator, validator_code
) -> DocumentType:
    validator = document_type_with_string_validator.get_validator(code=validator_code)
    validator.add_rule(
        name=uuid4().hex,
        severity=choice(list(Severity)),
        rule=uuid4().hex,
        issue_message=uuid4().hex,
        need_warning_even_if_optional=fake.boolean(),
        for_each=fake.boolean(),
        for_any=fake.boolean(),
        check_optional_fields=fake.boolean(),
    )
    return document_type_with_string_validator


@pytest.fixture
def validation_result_repository(repositories):
    return repositories.validation_result()


@pytest.fixture
def auth_headers():
    return {"Authorization": "Bearer test_token"}


@pytest.fixture
def validators_for_cross_field_test():
    field_codes = ["field1", "field2"]
    validators = []

    for field_code in field_codes:
        validator = Validator(
            code=field_code,
            type_=ValidatorType(type=OperandType.STRING),
            is_required=False,
        )
        validators.append(validator)

    return validators


@pytest.fixture
def document_type_with_validators(document_type_id, tenant_id, validators_for_cross_field_test):
    document_type = DocumentType(
        id_=document_type_id,
        tenant_id=tenant_id,
        validators=validators_for_cross_field_test,
    )

    return document_type
