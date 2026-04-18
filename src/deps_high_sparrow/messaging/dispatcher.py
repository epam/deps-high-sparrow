import logging

from deps_message_flow.commands.consumer import (
    CommandDispatcher,
    CommandHandlersBuilder,
)
from deps_message_flow.events.subscriber import (
    DomainEventDispatcher,
    DomainEventHandlersBuilder,
)
from deps_message_flow.messaging.consumer import IMessageConsumer
from deps_message_flow.messaging.producer import IMessageProducer

from deps_high_sparrow.constants import (
    COMMANDS_QUEUE,
    COMMANDS_REPLIES_CHANNEL,
    DOCUMENT_TYPE_EXCHANGER,
    DOCUMENTS_EXCHANGER,
    EVENTS_QUEUE,
    EXTRACTION_EXCHANGER,
    VALIDATION_SERVICE_CHANNEL,
)

from .commands import GetDocumentTypesReply, PerformValidation
from .events import (
    DocumentTypeCreated,
    DocumentTypeDeleted,
    DocumentTypeFieldCreated,
    DocumentTypeFieldDeleted,
    DocumentTypeFieldUpdated,
    ExtractorFieldCreated,
    ExtractorFieldDeleted,
    ExtractorFieldUpdated,
)

_logger = logging.getLogger(__name__)


def make_message_dispatcher(
    subscriber: IMessageConsumer,
    producer: IMessageProducer,
) -> IMessageConsumer:
    from .handlers import (  # noqa: WPS433
        document_type_created_handler,
        document_type_deleted_handler,
        extraction_field_deleted_handler,
        extraction_field_deleted_handler_for_corleone,
        extraction_field_modified_handler,
        extraction_field_modified_handler_for_corleone,
        get_document_types_reply_handler,
        perform_validation_handler,
    )

    events_handlers = (
        DomainEventHandlersBuilder.for_aggregate_type(DOCUMENTS_EXCHANGER)
        .on_event(DocumentTypeFieldCreated, extraction_field_modified_handler_for_corleone)
        .on_event(DocumentTypeFieldUpdated, extraction_field_modified_handler_for_corleone)
        .on_event(DocumentTypeFieldDeleted, extraction_field_deleted_handler_for_corleone)
        .and_for_aggregate_type(DOCUMENT_TYPE_EXCHANGER)
        .on_event(DocumentTypeCreated, document_type_created_handler)
        .on_event(DocumentTypeDeleted, document_type_deleted_handler)
        .and_for_aggregate_type(EXTRACTION_EXCHANGER)
        .on_event(ExtractorFieldCreated, extraction_field_modified_handler)
        .on_event(ExtractorFieldUpdated, extraction_field_modified_handler)
        .on_event(ExtractorFieldDeleted, extraction_field_deleted_handler)
        .for_queue(EVENTS_QUEUE)
        .build()
    )

    commands_handlers = (
        CommandHandlersBuilder.from_channel(COMMANDS_REPLIES_CHANNEL)
        .on_message(GetDocumentTypesReply, get_document_types_reply_handler)
        .and_from_channel(VALIDATION_SERVICE_CHANNEL)
        .on_message(PerformValidation, perform_validation_handler)
        .for_queue(COMMANDS_QUEUE)
        .build()
    )

    ded = DomainEventDispatcher(events_handlers, subscriber)
    ded.initialize()

    cd = CommandDispatcher(commands_handlers, subscriber, producer)
    cd.initialize()

    _logger.info("Start consuming....")

    return subscriber
