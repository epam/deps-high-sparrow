import pytest

from deps_high_sparrow.application import ValidatorService
from deps_high_sparrow.domain import DocumentType, IDocumentTypeRepository
from deps_high_sparrow.domain.exceptions import ValidatorNotFound


def test_upsert_new_validator_for_existing_doc_type__created(
    fake_document_type_repository: IDocumentTypeRepository,
    validator_service: ValidatorService,
    document_type: DocumentType,
    extraction_string_field,
):
    fake_document_type_repository.save(document_type)

    validator_service.save_validator(
        document_type_id=document_type.id(), tenant_id=document_type.tenant_id(), field=extraction_string_field
    )

    saved_document_type = fake_document_type_repository.document_type_of_id(
        document_type_id=document_type.id(),
        tenant_id=document_type.tenant_id(),
    )

    created_validator = saved_document_type.get_validator(code=extraction_string_field["code"])

    assert created_validator.code() == extraction_string_field["code"]
    assert created_validator.type_.type == extraction_string_field["field_type"]
    assert created_validator.is_required == extraction_string_field["required"]


def test_upsert_new_validator_for_non_existing_doc_type__no_error(
    validator_service: ValidatorService,
    extraction_string_field,
):
    validator_service.save_validator(
        document_type_id="non-existing-document-type-id",
        tenant_id="non-existing-tenant-id",
        field=extraction_string_field,
    )


def test_upsert_existing_validator__updated(
    fake_document_type_repository: IDocumentTypeRepository,
    validator_service: ValidatorService,
    document_type_with_string_validator,
    validator_code,
    extraction_string_field,
):
    fake_document_type_repository.save(document_type_with_string_validator)
    extraction_string_field["code"] = validator_code
    extraction_string_field["required"] = not extraction_string_field["required"]

    validator_service.save_validator(
        document_type_id=document_type_with_string_validator.id(),
        tenant_id=document_type_with_string_validator.tenant_id(),
        field=extraction_string_field,
    )

    saved_document_type = fake_document_type_repository.document_type_of_id(
        document_type_id=document_type_with_string_validator.id(),
        tenant_id=document_type_with_string_validator.tenant_id(),
    )

    updated_validator = saved_document_type.get_validator(code=validator_code)

    assert updated_validator.code() == validator_code
    assert updated_validator.type_.type == extraction_string_field["field_type"]
    assert updated_validator.is_required == extraction_string_field["required"]


def test_remove_existing_validator__ok(
    fake_document_type_repository: IDocumentTypeRepository,
    validator_service: ValidatorService,
    document_type_with_string_validator,
    validator_code,
):
    fake_document_type_repository.save(document_type_with_string_validator)

    validator_service.remove_validator(
        document_type_id=document_type_with_string_validator.id(),
        tenant_id=document_type_with_string_validator.tenant_id(),
        field_code=validator_code,
    )

    saved_document_type = fake_document_type_repository.document_type_of_id(
        document_type_id=document_type_with_string_validator.id(),
        tenant_id=document_type_with_string_validator.tenant_id(),
    )

    with pytest.raises(ValidatorNotFound):
        saved_document_type.get_validator(code=validator_code)


def test_remove_non_existing_validator__no_error(validator_service: ValidatorService):
    validator_service.remove_validator(
        document_type_id="non-existing-document-type-id",
        tenant_id="non-existing-tenant-id",
        field_code="non-existing-field-code",
    )
