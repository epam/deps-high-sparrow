from typing import Union

from dependency_injector.wiring import Provide, inject
from deps_message_flow.events.subscriber.domain_event_envelope import (
    DomainEventEnvelope,
)

from deps_high_sparrow.api.auth import get_current_user_tenant
from deps_high_sparrow.application import ValidatorService
from deps_high_sparrow.containers import Containers
from deps_high_sparrow.shared import ExtractionField

from .. import DocumentTypeFieldUpdated
from ..events import DocumentTypeFieldCreated, ExtractionFieldUpsertedEvent

__all__ = ["extraction_field_modified_handler", "extraction_field_modified_handler_for_corleone"]


@inject
def extraction_field_modified_handler(
    dee: DomainEventEnvelope[ExtractionFieldUpsertedEvent],
    validator_service: ValidatorService = Provide[Containers.application.validator],
) -> None:
    validator_service.save_validator(
        dee.event.document_type_code,
        tenant_id=get_current_user_tenant(),
        field=ExtractionField(
            code=dee.event.code,
            field_type=dee.event.field_type,
            required=dee.event.required,
            field_data=dee.event.description,
        ),
    )


@inject
def extraction_field_modified_handler_for_corleone(
    dee: DomainEventEnvelope[Union[DocumentTypeFieldCreated, DocumentTypeFieldUpdated]],
    validator_service: ValidatorService = Provide[Containers.application.validator],
) -> None:
    validator_service.save_validator(
        dee.event.document_type_code,
        tenant_id=get_current_user_tenant(),
        field=ExtractionField(
            code=dee.event.field["code"],
            field_type=dee.event.field["field_type"],
            required=dee.event.field["required"],
            field_data=dee.event.field["field_meta"],
        ),
    )
