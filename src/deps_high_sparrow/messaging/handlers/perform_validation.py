import logging

from dependency_injector.wiring import Provide, inject
from deps_message_flow.commands.consumer.command_message import CommandMessage
from deps_message_flow.messaging.common import IMessage

from deps_high_sparrow.api.auth import get_current_user_tenant
from deps_high_sparrow.application import ValidationResultService
from deps_high_sparrow.containers import Containers

from ..commands import PerformValidation, PerformValidationReply
from .participant_reply_builder import ParticipantReplyBuilder

__all__ = ["perform_validation_handler"]

_logger = logging.getLogger(__name__)


@inject
def perform_validation_handler(
    command_message: CommandMessage[PerformValidation],
    service: ValidationResultService = Provide[Containers.application.validation_result],
) -> list[IMessage]:
    command = command_message.command
    document_id = command.document_id
    tenant_id = get_current_user_tenant()

    _logger.info("Starting validation for document %s", document_id)
    try:
        result = service.create_validation_result(
            document_id=document_id,
            document_type_id=command.document_type_id,
            tenant_id=tenant_id,
        )
        _logger.info("Validation result: %s", result.is_valid)

        return [ParticipantReplyBuilder.with_success(PerformValidationReply(result=result.is_valid))]

    except Exception as error:
        _logger.error("[perform_validation] Error occurred: %s", error, exc_info=True)

        return [ParticipantReplyBuilder.with_success(PerformValidationReply(result=False))]
