from dependency_injector.wiring import Provide, inject
from deps_message_flow.events.subscriber.domain_event_envelope import (
    DomainEventEnvelope,
)

from deps_high_sparrow.application import DocumentTypeService
from deps_high_sparrow.containers import Containers

__all__ = ["document_type_deleted_handler"]


@inject
def document_type_deleted_handler(
    dee: DomainEventEnvelope,
    service: DocumentTypeService = Provide[Containers.application.document_type],
) -> None:
    service.delete_document_type(
        document_type_id=dee.event.document_type,
        tenant_id=dee.event.tenant,
    )
