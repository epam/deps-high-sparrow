import logging
from uuid import uuid4

from deps_message_flow.events.publisher import DomainEventPublisher

from deps_high_sparrow.constants import DOCUMENTS_EXCHANGER
from deps_high_sparrow.domain.exceptions import (
    DocumentTypeNotFound,
    ValidationResultNotFound,
)
from deps_high_sparrow.domain.model import (
    DocumentArtifact,
    DocumentType,
    IDocumentTypeRepository,
    IValidationResultRepository,
    ValidationResult,
)

from .external_validation_service import ExternalValidationService
from .iextraction import IExtractionProxy

__all__ = ["ValidationResultService"]


class ValidationResultService:
    def __init__(
        self,
        validation_result_repository: IValidationResultRepository,
        extraction_proxy: IExtractionProxy,
        external_validation_service: ExternalValidationService,
        document_type_repository: IDocumentTypeRepository,
        domain_event_publisher: DomainEventPublisher,
    ):
        self._validation_result_repository = validation_result_repository
        self._extraction_proxy = extraction_proxy
        self._external_validation_service = external_validation_service
        self._document_type_repository = document_type_repository
        self._logger = logging.getLogger(self.__class__.__name__)
        self._publisher = domain_event_publisher

    def find_validation_result(
        self,
        entity_id: str,
        tenant_id: str,
    ) -> ValidationResult:
        validation_result = self._get_validation_result(document_id=entity_id, tenant_id=tenant_id)
        if validation_result is None:
            raise ValidationResultNotFound(entity_id)

        return validation_result

    def create_validation_result(
        self, document_id: str, document_type_id: str | None, tenant_id: str
    ) -> ValidationResult:
        if document_type_id is None:
            validation_result = ValidationResult(id=document_id, tenant_id=tenant_id)
        else:
            document_type = self._get_document_type(document_type_id=document_type_id, tenant_id=tenant_id)
            value_units = self._extraction_proxy.get_value_units_from_extracted_data(document_id)
            document_artifacts = [DocumentArtifact(code=unit.code, value=unit.value) for unit in value_units]

            document_type.record_local_validation(document_id=document_id, document_artifacts=document_artifacts)

            if document_type.has_external_validators:
                self._external_validation_service.perform_validation(
                    document_id=document_id, document_type=document_type
                )

            validation_result = document_type.derive_validation_result()

        self._validation_result_repository.save(validation_result)

        self._publish_events(validation_result)

        return validation_result

    def validate_field(
        self,
        document_id: str,
        document_type_id: str,
        field_code: str,
        tenant_id: str,
    ) -> ValidationResult:
        document_type = self._get_document_type(document_type_id=document_type_id, tenant_id=tenant_id)

        field_codes = document_type.fields_to_validate_with(field_code)

        value_units = self._extraction_proxy.get_document_artifacts_for_fields(
            document_id=document_id,
            field_codes=field_codes,
        )
        document_artifacts = [
            DocumentArtifact(code=value_unit.code, value=value_unit.value) for value_unit in value_units
        ]

        validation_result = self._get_validation_result(document_id=document_id, tenant_id=tenant_id)

        document_type.record_field_validation(
            document_id=document_id,
            field_code=field_code,
            document_artifacts=document_artifacts,
            validation_result=validation_result,
        )

        validation_result = document_type.derive_validation_result()

        self._validation_result_repository.save(validation_result)

        return validation_result

    def _get_document_type(self, document_type_id: str, tenant_id: str) -> DocumentType:
        document_type = self._document_type_repository.document_type_of_id(
            document_type_id=document_type_id,
            tenant_id=tenant_id,
        )

        if document_type is None:
            raise DocumentTypeNotFound(document_type_id)

        return document_type

    def _get_validation_result(self, document_id: str, tenant_id: str) -> ValidationResult | None:
        return self._validation_result_repository.validation_result_of_id(
            entity_id=document_id,
            tenant_id=tenant_id,
        )

    def _publish_events(self, validation_result: ValidationResult) -> None:
        self._publisher.publish(
            aggregate_type=DOCUMENTS_EXCHANGER,
            aggregate_id=validation_result.id(),
            domain_events=validation_result.events,
            headers={"ID": uuid4().hex},
        )
