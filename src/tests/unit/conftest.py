from random import choice
from typing import Literal
from uuid import uuid4

import pytest
from faker import Faker

from deps_high_sparrow.api import auth
from deps_high_sparrow.application import FieldType
from deps_high_sparrow.constants import MAX_EXTERNAL_VALIDATORS
from deps_high_sparrow.domain import (
    CrossFieldIssueMessage,
    CrossFieldValidator,
    OperandType,
    Validator,
    ValidatorType,
)
from deps_high_sparrow.domain.model import (
    DocumentType,
    EntityCode,
    ExternalValidator,
    Issue,
    Issues,
    IssueType,
    Position,
    RawIssue,
    Severity,
    ValidationResult,
)
from deps_high_sparrow.infrastructure.access_management import user
from deps_high_sparrow.infrastructure.proxies import (
    ExternalValidationProxy,
    ExtractedDataValueUnit,
    ExtractionProxy,
)
from deps_high_sparrow.shared import ExtractionField
from tests.factories.cross_field_issue_message import CrossFieldIssueMessageFactory
from tests.factories.cross_field_validator import CrossFieldValidatorFactory
from tests.fakes import (
    FakeDocumentTypeRepository,
    FakeExtractionProxy,
    FakeValidationResultRepository,
)

fake = Faker()


@pytest.fixture
def postgres_datasource_mock(mocker, containers):
    mock = mocker.Mock(containers.datasources.postgres_datasource())
    containers.datasources.postgres_datasource.override(mock)

    yield mock

    containers.datasources.reset_override()


@pytest.fixture(autouse=True)
def fake_document_type_repository(containers):
    with containers.repositories.document_type.override(FakeDocumentTypeRepository()):
        yield containers.repositories.document_type()


@pytest.fixture(autouse=True)
def fake_validation_result_repository(containers):
    with containers.reset_singletons(), containers.repositories.validation_result.override(
        FakeValidationResultRepository()
    ):
        yield containers.repositories.validation_result()


@pytest.fixture
def rule_service(application, fake_document_type_repository):
    yield application.rule()


@pytest.fixture()
def rule_service_mock(application, mocker):
    with application.rule.override(mocker.Mock(application.rule.cls)) as service:
        yield service()


@pytest.fixture
def document_type_service(application, fake_document_type_repository):
    yield application.document_type()


@pytest.fixture()
def document_type_service_mock(application, mocker):
    with application.document_type.override(mocker.Mock(application.document_type.cls)) as service:
        yield service()


@pytest.fixture
def validation_result_service(application, fake_validation_result_repository):
    with application.reset_singletons():
        yield application.validation_result()


@pytest.fixture()
def validation_result_service_mock(application, mocker):
    with application.validation_result.override(mocker.Mock(application.validation_result.cls)) as service:
        yield service()


@pytest.fixture
def validator_service(application, fake_document_type_repository):
    yield application.validator()


@pytest.fixture
def validator_service_mock(application, mocker):
    with application.validator.override(mocker.Mock(application.validator.cls)) as service:
        yield service()


@pytest.fixture(autouse=True)
def external_validation_proxy_mock(external_services, mocker) -> ExternalValidationProxy:
    with external_services.external_validation.override(
        mocker.Mock(external_services.external_validation.cls)
    ) as proxy:
        yield proxy()


@pytest.fixture
def fake_extraction_proxy(external_services):
    with external_services.extraction.override(FakeExtractionProxy()):
        yield external_services.extraction()


@pytest.fixture
def value_units_for_validator(validator_code):
    return [
        ExtractedDataValueUnit(code=validator_code, value="some_value"),
    ]


@pytest.fixture
def entity_code_1():
    return uuid4().hex


@pytest.fixture
def entity_code_2():
    return uuid4().hex


@pytest.fixture
def entity_code_3():
    return uuid4().hex


@pytest.fixture
def entity_code_4():
    return uuid4().hex


@pytest.fixture
def validation_result_id() -> str:
    return uuid4().hex


@pytest.fixture
def field_code() -> str:
    return uuid4().hex


@pytest.fixture
def this_user(tenant_id):
    return dict(
        subject="Leo",
        groups=[tenant_id],
        token="token",
        roles=[],
        organisation=tenant_id,
    )


@pytest.fixture(autouse=True)
def set_this_user(this_user):
    user.set(this_user)


@pytest.fixture(autouse=True)
def mocked_middleware(monkeypatch, mocker):
    monkeypatch.setattr(auth, "set_user_from_token", mocker.Mock({}))


@pytest.fixture
def validator_code() -> str:
    return uuid4().hex


@pytest.fixture
def external_validator_url() -> str:
    return fake.url()


@pytest.fixture
def external_validator_name() -> str:
    return uuid4().hex


@pytest.fixture
def external_validator(external_validator_name, external_validator_url):
    return ExternalValidator(
        name=external_validator_name,
        url=external_validator_url,
    )


@pytest.fixture
def rule_name() -> str:
    return uuid4().hex


@pytest.fixture
def rule_name_with_slash() -> str:
    return f"validator/{uuid4().hex}"


@pytest.fixture
def rule_severity() -> Severity:
    return choice(list(Severity))


@pytest.fixture
def rule_text() -> str:
    return uuid4().hex


@pytest.fixture
def rule_issue_message() -> str:
    return uuid4().hex


@pytest.fixture
def rule_description() -> str:
    return uuid4().hex


@pytest.fixture
def rule_need_warning_even_if_optional() -> bool:
    return fake.boolean()


@pytest.fixture
def rule_for_each() -> bool:
    return fake.boolean()


@pytest.fixture
def rule_for_any() -> bool:
    return fake.boolean()


@pytest.fixture
def rule_check_optional_fields() -> bool:
    return fake.boolean()


@pytest.fixture
def document_type(document_type_id, tenant_id) -> DocumentType:
    return DocumentType(id_=document_type_id, tenant_id=tenant_id)


@pytest.fixture
def document_type_with_string_validator(document_type, validator_code) -> DocumentType:
    document_type.add_string_validator(code=validator_code).with_description().is_required().build()
    return document_type


@pytest.fixture
def document_type_with_number_validator(document_type, validator_code) -> DocumentType:
    document_type.add_number_validator(code=validator_code).is_required().build()
    return document_type


@pytest.fixture
def document_type_with_key_value_validator(document_type, validator_code) -> DocumentType:
    # fmt: off
    document_type \
        .add_key_value_validator(validator_code) \
        .with_description() \
        .with_key() \
        .with_enum_value() \
        .with_options(options=["op1", "op2"]) \
        .is_required() \
        .build()
    # fmt: on
    return document_type


@pytest.fixture
def document_type_with_list_of_key_value_validators(document_type, validator_code) -> DocumentType:
    # fmt: off
    document_type \
        .add_list_validator(validator_code) \
        .with_description() \
        .for_key_value_item() \
        .with_key() \
        .with_string_value() \
        .is_required() \
        .build()
    # fmt: on
    return document_type


@pytest.fixture
def document_type_with_table_validator(document_type, validator_code) -> DocumentType:
    # fmt: off
    document_type.add_table_validator(validator_code) \
        .with_description() \
        .for_number_column(index=0, is_required=True) \
        .for_date_column(index=1, is_required=False) \
        .for_number_column(index=2, is_required=False) \
        .for_string_column(index=3, is_required=True) \
        .for_date_column(index=4, is_required=False) \
        .for_number_column(index=5, is_required=False) \
        .is_required() \
        .build()
    # fmt: on
    return document_type


@pytest.fixture
def document_type_with_string_validator_and_one_rule(
    document_type_with_string_validator,
    validator_code,
    rule_name,
    rule_severity,
    rule_text,
    rule_issue_message,
    rule_need_warning_even_if_optional,
    rule_for_each,
    rule_for_any,
    rule_check_optional_fields,
) -> DocumentType:
    validator = document_type_with_string_validator.get_validator(code=validator_code)
    validator.add_rule(
        name=rule_name,
        severity=rule_severity,
        rule=rule_text,
        issue_message=rule_issue_message,
        need_warning_even_if_optional=rule_need_warning_even_if_optional,
        for_each=rule_for_each,
        for_any=rule_for_any,
        check_optional_fields=rule_check_optional_fields,
    )
    return document_type_with_string_validator


@pytest.fixture
def document_type_with_string_validator_and_one_rule_with_slash(
    document_type_with_string_validator,
    validator_code,
    rule_name_with_slash,
    rule_severity,
    rule_text,
    rule_issue_message,
    rule_need_warning_even_if_optional,
    rule_for_each,
    rule_for_any,
    rule_check_optional_fields,
) -> DocumentType:
    validator = document_type_with_string_validator.get_validator(code=validator_code)
    validator.add_rule(
        name=rule_name_with_slash,
        severity=rule_severity,
        rule=rule_text,
        issue_message=rule_issue_message,
        need_warning_even_if_optional=rule_need_warning_even_if_optional,
        for_each=rule_for_each,
        for_any=rule_for_any,
        check_optional_fields=rule_check_optional_fields,
    )
    return document_type_with_string_validator


@pytest.fixture
def document_type_with_external_validator(
    document_type,
    external_validator_name,
    external_validator,
) -> DocumentType:
    document_type._external_validators[external_validator_name] = external_validator
    return document_type


@pytest.fixture
def document_type_with_maximum_external_validators(document_type, external_validator_factory) -> DocumentType:
    for _ in range(MAX_EXTERNAL_VALIDATORS):
        name = uuid4().hex
        document_type._external_validators[name] = external_validator_factory(name=name)
    return document_type


@pytest.fixture
def position_kv_id() -> Literal["key", "value"]:
    return choice(list(["key", "value"]))


@pytest.fixture
def position_for_kv_id(position_kv_id) -> Position:
    return Position.for_kv_id(kv_id=position_kv_id, index=fake.pyint())


@pytest.fixture
def position_for_cell() -> Position:
    return Position.for_cell(column=fake.pyint(), row=fake.pyint(), index=fake.pyint())


@pytest.fixture
def error_validation_issue() -> Issue:
    return Issue(
        severity=Severity.ERROR,
        type=choice(list(IssueType)),
        message=fake.word(),
    )


@pytest.fixture
def warning_validation_issue() -> Issue:
    return Issue(
        severity=Severity.WARNING,
        type=choice(list(IssueType)),
        message=fake.word(),
    )


@pytest.fixture
def raw_issue() -> RawIssue:
    return RawIssue(
        message=fake.word(),
        column=fake.pyint(),
        row=fake.pyint(),
        index=fake.pyint(),
        kv_id=position_kv_id,
    )


@pytest.fixture
def validation_issues(raw_issue) -> Issues:
    issues = Issues(code=EntityCode(uuid4().hex))
    issues.add(
        type=choice(list(IssueType)),
        errors=[raw_issue],
        warnings=[raw_issue],
    )
    return issues


@pytest.fixture
def validation_result(validation_result_id, tenant_id) -> ValidationResult:
    return ValidationResult(id=validation_result_id, tenant_id=tenant_id)


@pytest.fixture
def validation_result_with_issues(validation_result, validation_issues) -> ValidationResult:
    validation_result.add_issues(validation_issues)
    return validation_result


@pytest.fixture
def extraction_field_code() -> str:
    return uuid4().hex


@pytest.fixture
def extraction_string_field_type() -> str:
    return FieldType.STRING.value


@pytest.fixture
def extraction_string_field_data() -> dict:
    return {"char_blacklist": "i", "char_whitelist": "j"}


@pytest.fixture
def extraction_field_required() -> bool:
    return fake.boolean()


@pytest.fixture
def extraction_string_field(
    extraction_field_code,
    extraction_string_field_type,
    extraction_string_field_data,
    extraction_field_required,
) -> ExtractionField:
    return ExtractionField(
        code=extraction_field_code,
        field_type=extraction_string_field_type,
        required=extraction_field_required,
        field_data=extraction_string_field_data,
    )


@pytest.fixture
def extraction_proxy(external_services) -> ExtractionProxy:
    return external_services.extraction()


@pytest.fixture
def cross_field_issue_message():
    return CrossFieldIssueMessageFactory()


@pytest.fixture
def cross_field_validator():
    return CrossFieldValidatorFactory()


@pytest.fixture
def document_type_with_cross_field_validator(document_type, cross_field_validator):
    document_type._cross_field_validators = {cross_field_validator.id(): cross_field_validator}
    return document_type


@pytest.fixture
def document_type_with_every_validator(
    document_type: DocumentType,
    external_validator: ExternalValidator,
    cross_field_validator: CrossFieldValidator,
    validator_code: str,
) -> DocumentType:
    document_type._cross_field_validators = {cross_field_validator.id(): cross_field_validator}
    document_type._external_validators = {external_validator.name: external_validator}
    document_type.add_string_validator(code=validator_code).with_description().is_required().build()
    return document_type


@pytest.fixture
def cross_field_validator_id(cross_field_validator):
    return cross_field_validator.id()


@pytest.fixture
def cross_field_validator_name():
    return "test_validator"


@pytest.fixture
def cross_field_validator_rule():
    return "Ffield1 == Ffield2"


@pytest.fixture
def cross_field_validator_description():
    return "Test validator description"


@pytest.fixture
def cross_field_validator_severity():
    return Severity.ERROR


@pytest.fixture
def cross_field_validated_fields():
    return [EntityCode("field1"), EntityCode("field2")]


@pytest.fixture
def cross_field_issue_message_text():
    return "Fields ${field1} and ${field2} must match"


@pytest.fixture
def cross_field_dependent_fields():
    return [EntityCode("field1"), EntityCode("field2")]


@pytest.fixture
def cross_field_issue_message_fixture(cross_field_issue_message_text, cross_field_dependent_fields):
    return CrossFieldIssueMessage(
        message=cross_field_issue_message_text,
        dependent_fields=cross_field_dependent_fields,
    )


@pytest.fixture
def crossfield_validator_data():
    return {
        "name": "validator1",
        "description": "test description",
        "rule": "Ffield1 > Ffield2",
        "severity": Severity.ERROR,
        "validated_fields": ["field1", "field2"],
        "issue_message": "Field 1 should be greater than Field 2",
        "dependent_fields": ["field1", "field2"],
        "for_each": False,
        "for_any": False,
    }


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


@pytest.fixture
def document_type_with_all_validators(document_type_id, tenant_id):
    field_codes = ["field1", "field2", "field3", "field4"]
    validators = []

    for field_code in field_codes:
        validator = Validator(
            code=field_code,
            type_=ValidatorType(type=OperandType.STRING),
            is_required=False,
        )
        validators.append(validator)

    document_type = DocumentType(
        id_=document_type_id,
        tenant_id=tenant_id,
        validators=validators,
    )

    cross_field_validator_id = document_type.add_cross_field_validator(
        name="test_validator",
        description="Test validator description",
        rule="Ffield1 == Ffield2",
        severity=Severity.ERROR,
        validated_fields=["field1", "field2"],
        issue_message="Fields ${field1} and ${field2} must match",
        dependent_fields=["field1", "field2"],
    )

    return document_type, cross_field_validator_id
