from uuid import uuid4

import pytest

from deps_high_sparrow.application import ValidationResultService
from deps_high_sparrow.domain.exceptions import (
    DocumentTypeNotFound,
    ValidationResultNotFound,
)
from deps_high_sparrow.domain.model import (
    DocumentType,
    IDocumentTypeRepository,
    IValidationResultRepository,
)
from deps_high_sparrow.infrastructure.proxies.external_validation import (
    ExternalValidationClientError,
    ExternalValidatorResponse,
)
from tests.data.external_validation_result_data import EXTERNAL_VALIDATION_RESPONSE


class TestValidationResultService:
    def test_find_validation_result__ok(
        self,
        validation_result_service,
        validation_result_with_issues,
        fake_validation_result_repository: IValidationResultRepository,
    ):
        fake_validation_result_repository.save(validation_result_with_issues)

        validation_result_from_service = validation_result_service.find_validation_result(
            entity_id=validation_result_with_issues.id(),
            tenant_id=validation_result_with_issues.tenant_id(),
        )

        assert validation_result_from_service == validation_result_from_service

    def test_find_validation_result_not_found__raised(
        self,
        validation_result_service,
        validation_result_with_issues,
    ):
        with pytest.raises(ValidationResultNotFound):
            validation_result_service.find_validation_result(
                entity_id=validation_result_with_issues.id(),
                tenant_id=validation_result_with_issues.tenant_id(),
            )

    @pytest.mark.validation_result_creation
    def test_create_validation_result__document_type_doesnt_exist__error(
        self,
        validation_result_service: ValidationResultService,
    ):
        with pytest.raises(DocumentTypeNotFound):
            validation_result_service.create_validation_result(
                document_id=uuid4().hex,
                document_type_id=uuid4().hex,
                tenant_id=uuid4().hex,
            )

    @pytest.mark.validation_result_creation
    def test_create_validation_result__document_type_id__is_none__ok(
        self,
        validation_result_service: ValidationResultService,
        fake_document_type_repository: IDocumentTypeRepository,
        document_type_with_external_validator: DocumentType,
        tenant_id,
        document_id,
    ):
        fake_document_type_repository.save(document_type_with_external_validator)

        validation_result = validation_result_service.create_validation_result(
            document_id=document_id,
            document_type_id=None,
            tenant_id=tenant_id,
        )

        assert len(validation_result.issues) == 0

    @pytest.mark.validation_result_creation
    def test_create_validation_result__document_type_with_external_validators__ok(
        self,
        validation_result_service: ValidationResultService,
        fake_document_type_repository: IDocumentTypeRepository,
        document_type_with_external_validator: DocumentType,
        external_validation_proxy_mock,
        get_edata_request_mock,
        tenant_id,
        document_id,
    ):
        fake_document_type_repository.save(document_type_with_external_validator)
        external_validation_proxy_mock.validate_document.return_value = ExternalValidatorResponse.from_raw_response(
            EXTERNAL_VALIDATION_RESPONSE
        )

        validation_result = validation_result_service.create_validation_result(
            document_id=document_id,
            document_type_id=document_type_with_external_validator.id(),
            tenant_id=tenant_id,
        )

        assert len(validation_result.issues) == 3

    @pytest.mark.validation_result_creation
    def test_create_validation_result__document_type_with_external_validators__service_not_available__skipped(
        self,
        validation_result_service: ValidationResultService,
        fake_document_type_repository: IDocumentTypeRepository,
        document_type_with_external_validator: DocumentType,
        external_validation_proxy_mock,
        get_edata_request_mock,
        tenant_id,
        document_id,
    ):
        fake_document_type_repository.save(document_type_with_external_validator)

        external_validation_proxy_mock.validate_document.side_effect = ExternalValidationClientError("Client error")

        validation_result = validation_result_service.create_validation_result(
            document_id=document_id,
            document_type_id=document_type_with_external_validator.id(),
            tenant_id=tenant_id,
        )

        assert len(validation_result.issues) == 0

    def test_validate_field__document_type_not_found__raises(
        self,
        validation_result_service,
        document_id,
        tenant_id,
    ):
        with pytest.raises(DocumentTypeNotFound):
            validation_result_service.validate_field(
                document_id=document_id,
                document_type_id=uuid4().hex,
                field_code="any_field",
                tenant_id=tenant_id,
            )

    def test_validate_field__no_existing_result__creates_new(
        self,
        fake_extraction_proxy,
        validation_result_service,
        saved_document_type_with_field_validators,
        document_id,
        tenant_id,
        entity_code_1,
        value_units_field1_only,
    ):
        fake_extraction_proxy.set_field_value_units(value_units_field1_only)

        result = validation_result_service.validate_field(
            document_id=document_id,
            document_type_id=saved_document_type_with_field_validators.id(),
            field_code=entity_code_1,
            tenant_id=tenant_id,
        )

        assert result is not None
        assert result.id() == document_id
        assert entity_code_1 in result.issues

    def test_validate_field__existing_result__updates_it(
        self,
        fake_extraction_proxy,
        validation_result_service,
        fake_validation_result_repository,
        saved_document_type_with_field_validators,
        document_id,
        tenant_id,
        entity_code_1,
        value_units_field1_only,
        existing_validation_result,
    ):
        fake_validation_result_repository.save(existing_validation_result)
        fake_extraction_proxy.set_field_value_units(value_units_field1_only)

        result = validation_result_service.validate_field(
            document_id=document_id,
            document_type_id=saved_document_type_with_field_validators.id(),
            field_code=entity_code_1,
            tenant_id=tenant_id,
        )

        assert result is existing_validation_result
        assert entity_code_1 in result.issues

    def test_validate_field__with_cross_field_validators__includes_cross_field_issues(
        self,
        fake_extraction_proxy,
        validation_result_service,
        saved_document_type_with_cross_field_rules,
        document_id,
        tenant_id,
        entity_code_1,
        value_units_two_fields,
    ):
        fake_extraction_proxy.set_field_value_units(value_units_two_fields)

        result = validation_result_service.validate_field(
            document_id=document_id,
            document_type_id=saved_document_type_with_cross_field_rules.id(),
            field_code=entity_code_1,
            tenant_id=tenant_id,
        )

        assert result is not None
        assert entity_code_1 in result.issues
        assert len(result.cross_field_issues) > 0

    def test_validate_field__field_without_cross_field__no_cross_field_issues(
        self,
        fake_extraction_proxy,
        validation_result_service,
        saved_document_type_with_cross_field_rules,
        document_id,
        tenant_id,
        entity_code_3,
        value_units_field3_only,
    ):
        fake_extraction_proxy.set_field_value_units(value_units_field3_only)

        result = validation_result_service.validate_field(
            document_id=document_id,
            document_type_id=saved_document_type_with_cross_field_rules.id(),
            field_code=entity_code_3,
            tenant_id=tenant_id,
        )

        assert result is not None
        assert len(result.cross_field_issues) == 0

    def test_validate_field__result_is_saved(
        self,
        fake_extraction_proxy,
        validation_result_service,
        fake_validation_result_repository,
        saved_document_type_with_field_validators,
        document_id,
        tenant_id,
        entity_code_1,
        value_units_field1_only,
    ):
        fake_extraction_proxy.set_field_value_units(value_units_field1_only)

        result = validation_result_service.validate_field(
            document_id=document_id,
            document_type_id=saved_document_type_with_field_validators.id(),
            field_code=entity_code_1,
            tenant_id=tenant_id,
        )

        saved = fake_validation_result_repository.validation_result_of_id(
            entity_id=document_id,
            tenant_id=tenant_id,
        )
        assert saved is not None
        assert saved.id() == result.id()
