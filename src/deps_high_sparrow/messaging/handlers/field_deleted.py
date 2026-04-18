from dependency_injector.wiring import Provide, inject
from deps_message_flow.events.subscriber.domain_event_envelope import (
    DomainEventEnvelope,
)

from deps_high_sparrow.api.auth import get_current_user_tenant
from deps_high_sparrow.application import ValidatorService
from deps_high_sparrow.containers import Containers

from ..events import DocumentTypeFieldDeleted, ExtractorFieldDeleted

__all__ = ["extraction_field_deleted_handler", "extraction_field_deleted_handler_for_corleone"]


@inject
def extraction_field_deleted_handler(
    dee: DomainEventEnvelope[ExtractorFieldDeleted],
    validator_service: ValidatorService = Provide[Containers.application.validator],
) -> None:
    validator_service.remove_validator(
        dee.event.document_type_code, tenant_id=get_current_user_tenant(), field_code=dee.event.code
    )


@inject
def extraction_field_deleted_handler_for_corleone(
    dee: DomainEventEnvelope[DocumentTypeFieldDeleted],
    validator_service: ValidatorService = Provide[Containers.application.validator],
) -> None:
    validator_service.remove_validator(
        dee.event.document_type_code, tenant_id=get_current_user_tenant(), field_code=dee.event.field_code
    )
