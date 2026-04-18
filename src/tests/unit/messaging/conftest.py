from uuid import uuid4

import pytest
from deps_message_flow.commands.common import CommandReplyOutcome
from deps_message_flow.commands.consumer import CommandMessage
from deps_message_flow.events.subscriber.domain_event_envelope import (
    DomainEventEnvelope,
)


@pytest.fixture
def get_document_types_success_reply_message(mocker):
    cm = mocker.Mock(CommandMessage)
    cm.message.get_required_header.return_value = CommandReplyOutcome.SUCCESS.name
    cm.command.document_types = [{"document_type_id": uuid4().hex, "tenant_id": uuid4().hex} for _ in range(5)]

    return cm


@pytest.fixture
def get_document_types_failed_reply_message(mocker):
    cm = mocker.Mock(CommandMessage)
    cm.message.get_required_header.return_value = CommandReplyOutcome.FAILURE.name
    cm.command.document_types = []

    return cm


@pytest.fixture
def document_type_created_envelope(mocker, document_type_id, tenant_id):
    dee = mocker.Mock(DomainEventEnvelope)
    dee.event.document_type = document_type_id
    dee.event.tenant = tenant_id
    return dee


@pytest.fixture
def document_type_deleted_envelope(mocker, document_type_id, tenant_id):
    dee = mocker.Mock(DomainEventEnvelope)
    dee.event.document_type = document_type_id
    dee.event.tenant = tenant_id
    return dee


@pytest.fixture
def extraction_field_created_envelope(mocker, document_type_id, tenant_id, extraction_string_field):
    dee = mocker.Mock(DomainEventEnvelope)
    dee.event.document_type_code = document_type_id
    dee.event.code = extraction_string_field["code"]
    dee.event.field_type = extraction_string_field["field_type"]
    dee.event.required = extraction_string_field["required"]
    dee.event.description = extraction_string_field["field_data"]

    return dee


@pytest.fixture
def extraction_field_created_envelope_for_corleone(
    mocker,
    document_type_id,
    tenant_id,
    extraction_field_dict_for_corleone,
):
    dee = mocker.Mock(DomainEventEnvelope)
    dee.event.document_type_code = document_type_id
    dee.event.field = extraction_field_dict_for_corleone

    return dee


@pytest.fixture
def extraction_field_deleted_envelope_for_corleone(mocker, document_type_id, tenant_id, extraction_field_code):
    dee = mocker.Mock(DomainEventEnvelope)
    dee.event.document_type_code = document_type_id
    dee.event.field_code = extraction_field_code

    return dee


@pytest.fixture
def extraction_field_deleted_envelope(mocker, document_type_id, tenant_id, extraction_field_code):
    dee = mocker.Mock(DomainEventEnvelope)
    dee.event.document_type_code = document_type_id
    dee.event.code = extraction_field_code

    return dee


@pytest.fixture
def extraction_field_updated_envelope_for_corleone(
    mocker,
    document_type_id,
    tenant_id,
    extraction_field_dict_for_corleone,
):
    dee = mocker.Mock(DomainEventEnvelope)
    dee.event.document_type_code = document_type_id
    dee.event.field = extraction_field_dict_for_corleone

    return dee


@pytest.fixture
def extraction_field_updated_envelope(
    mocker,
    document_type_id,
    tenant_id,
    extraction_string_field,
):
    dee = mocker.Mock(DomainEventEnvelope)
    dee.event.document_type_code = document_type_id
    dee.event.code = extraction_string_field["code"]
    dee.event.field_type = extraction_string_field["field_type"]
    dee.event.required = extraction_string_field["required"]
    dee.event.description = extraction_string_field["field_data"]

    return dee


@pytest.fixture
def extraction_field_dict_for_corleone(extraction_string_field):
    return {
        "code": extraction_string_field["code"],
        "field_type": extraction_string_field["field_type"],
        "required": extraction_string_field["required"],
        "field_meta": extraction_string_field["field_data"],
    }
