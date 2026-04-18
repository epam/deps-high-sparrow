from random import randint

import pytest

from deps_high_sparrow.domain import (
    CrossFieldIssueMessage,
    DocumentType,
    EntityCode,
    IDocumentTypeRepository,
    Severity,
)


def compare_document_types(type1: DocumentType, type2: DocumentType) -> None:
    assert type1 == type2
    assert type1.tenant_id == type2.tenant_id
    assert type1._validators == type2._validators
    assert type1._external_validators == type2._external_validators


@pytest.mark.document_type
def test_save_find_delete__ok(fake_document_type_repository: IDocumentTypeRepository, document_type: DocumentType):
    fake_document_type_repository.save(document_type)

    saved_type = fake_document_type_repository.document_type_of_id(
        document_type_id=document_type.id(),
        tenant_id=document_type.tenant_id(),
    )

    compare_document_types(document_type, saved_type)

    fake_document_type_repository.delete(
        document_type_id=document_type.id(),
        tenant_id=document_type.tenant_id(),
    )

    assert (
        fake_document_type_repository.document_type_of_id(
            document_type_id=document_type.id(),
            tenant_id=document_type.tenant_id(),
        )
        is None
    )


@pytest.mark.document_type
def test_save__type_exists__updated(fake_document_type_repository, document_type):
    fake_document_type_repository.save(document_type)

    document_type._validators["test"] = "test"
    document_type._external_validators["test"] = "test"
    fake_document_type_repository.save(document_type)

    saved_document_type = fake_document_type_repository.document_type_of_id(
        document_type_id=document_type.id(),
        tenant_id=document_type.tenant_id(),
    )

    assert saved_document_type._validators["test"] == "test"
    assert saved_document_type._external_validators["test"] == "test"


@pytest.mark.document_type
def test_save_new_all__ok(fake_document_type_repository: IDocumentTypeRepository, document_type_factory):
    document_type_batch_size = randint(1, 5)
    document_types = document_type_factory.build_batch(size=document_type_batch_size)
    fake_document_type_repository.save_new_all(document_types)

    for type_ in document_types:
        saved_document_type = fake_document_type_repository.document_type_of_id(
            document_type_id=type_.id(),
            tenant_id=type_.tenant_id(),
        )

        compare_document_types(type_, saved_document_type)


@pytest.mark.document_type
def test_save_new_all__types_exist__not_updated(fake_document_type_repository, document_type_factory):
    document_type_batch_size = randint(1, 5)
    document_types = document_type_factory.build_batch(size=document_type_batch_size)
    fake_document_type_repository.save_all(document_types)

    for type_ in document_types:
        type_._validators["test"] = "test"
        type_._external_validators["test"] = "test"
    fake_document_type_repository.save_new_all(document_types)

    for type_ in document_types:
        saved_type = fake_document_type_repository.document_type_of_id(
            document_type_id=type_.id(),
            tenant_id=type_.tenant_id(),
        )

        assert not saved_type.validators
        assert not saved_type._external_validators


@pytest.mark.document_type
def test_save_new__ok(fake_document_type_repository: IDocumentTypeRepository, document_type):
    fake_document_type_repository.save_new(document_type)

    saved_document_type = fake_document_type_repository.document_type_of_id(
        document_type_id=document_type.id(),
        tenant_id=document_type.tenant_id(),
    )

    compare_document_types(document_type, saved_document_type)


@pytest.mark.document_type
def test_save_new__type_exists__not_updated(fake_document_type_repository, document_type):
    fake_document_type_repository.save(document_type)
    document_type._validators["test"] = "test"
    document_type._external_validators["test"] = "test"

    fake_document_type_repository.save_new(document_type)

    saved_type = fake_document_type_repository.document_type_of_id(
        document_type_id=document_type.id(),
        tenant_id=document_type.tenant_id(),
    )

    assert not saved_type.validators
    assert not saved_type._external_validators


@pytest.mark.document_type
def test_delete__type_doesnt_exist__no_error(fake_document_type_repository, document_type):
    fake_document_type_repository.delete(
        document_type_id=document_type.id(),
        tenant_id=document_type.tenant_id(),
    )


@pytest.mark.document_type
def test_save_find_delete_with_cross_field_validators__ok(
    fake_document_type_repository: IDocumentTypeRepository,
    document_type_with_validators: DocumentType,
    cross_field_validator_name,
    cross_field_validator_description,
    cross_field_validator_rule,
    cross_field_validator_severity,
    cross_field_validated_fields,
    cross_field_issue_message_text,
    cross_field_dependent_fields,
):
    validated_fields_str = [field.value for field in cross_field_validated_fields]
    dependent_fields_str = [field.value for field in cross_field_dependent_fields]

    validator_id = document_type_with_validators.add_cross_field_validator(
        name=cross_field_validator_name,
        description=cross_field_validator_description,
        rule=cross_field_validator_rule,
        severity=cross_field_validator_severity,
        validated_fields=validated_fields_str,
        issue_message=cross_field_issue_message_text,
        dependent_fields=dependent_fields_str,
    )

    fake_document_type_repository.save(document_type_with_validators)

    saved_type = fake_document_type_repository.document_type_of_id(
        document_type_id=document_type_with_validators.id(),
        tenant_id=document_type_with_validators.tenant_id(),
    )

    assert len(saved_type.cross_field_validators) == 1
    saved_validator = saved_type.cross_field_validators[0]
    assert saved_validator.id() == validator_id
    assert saved_validator.name == cross_field_validator_name
    assert saved_validator.description == cross_field_validator_description
    assert saved_validator.rule == cross_field_validator_rule
    assert saved_validator.severity == cross_field_validator_severity
    assert [field.value for field in saved_validator.validated_fields] == validated_fields_str
    assert saved_validator.issue_message.message == cross_field_issue_message_text
    assert [field.value for field in saved_validator.issue_message.dependent_fields] == dependent_fields_str

    fake_document_type_repository.delete(
        document_type_id=document_type_with_validators.id(),
        tenant_id=document_type_with_validators.tenant_id(),
    )

    assert (
        fake_document_type_repository.document_type_of_id(
            document_type_id=document_type_with_validators.id(),
            tenant_id=document_type_with_validators.tenant_id(),
        )
        is None
    )


@pytest.mark.document_type
def test_save__add_cross_field_validator__ok(
    fake_document_type_repository: IDocumentTypeRepository,
    document_type_with_all_validators,
):
    document_type, cross_field_validator_id = document_type_with_all_validators

    fake_document_type_repository.save(document_type)

    new_validator_id = document_type.add_cross_field_validator(
        name="second_validator",
        description="Second validator description",
        rule="Ffield3 == Ffield4",
        severity=Severity.WARNING,
        validated_fields=["field3", "field4"],
        issue_message="Fields ${field3} and ${field4} must match",
        dependent_fields=["field3", "field4"],
    )

    fake_document_type_repository.save(document_type)

    saved_type = fake_document_type_repository.document_type_of_id(
        document_type_id=document_type.id(),
        tenant_id=document_type.tenant_id(),
    )

    assert len(saved_type.cross_field_validators) == 2  # Now we have 2 validators

    new_validator = next((v for v in saved_type.cross_field_validators if v.id() == new_validator_id), None)
    assert new_validator is not None
    assert new_validator.name == "second_validator"

    original_validator = next(
        (v for v in saved_type.cross_field_validators if v.id() == cross_field_validator_id), None
    )
    assert original_validator is not None
