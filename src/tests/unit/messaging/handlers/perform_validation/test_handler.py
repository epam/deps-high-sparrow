import json

import pytest
from deps_message_flow.commands.common import CommandReplyOutcome, ReplyMessageHeaders
from deps_message_flow.commands.consumer import CommandMessage
from deps_message_flow.messaging.common import IMessage
from pytest_mock import MockerFixture

from deps_high_sparrow.domain.events import BusinessRuleViolated
from deps_high_sparrow.domain.model import (
    CrossFieldValidator,
    DocumentType,
    EntityCode,
    IDocumentTypeRepository,
)
from deps_high_sparrow.infrastructure.proxies import ExtractedDataValueUnit
from deps_high_sparrow.messaging.handlers import perform_validation_handler
from tests.fakes import FakeDomainEventPublisher

FIRST_ELEMENT = 0


@pytest.mark.validation_result_creation
def test_perform_validation__validation_success__ok(
    fake_document_type_repository: IDocumentTypeRepository,
    document_type_with_string_validator: DocumentType,
    perform_validation_message: CommandMessage,
    get_right_edata_request_mock,
    document_id,
    tenant_id,
):
    fake_document_type_repository.save(document_type_with_string_validator)

    result = perform_validation_handler(perform_validation_message)

    result_message: IMessage = result[FIRST_ELEMENT]
    assert result_message.get_header(ReplyMessageHeaders.REPLY_OUTCOME) == CommandReplyOutcome.SUCCESS.value
    assert json.loads(result_message.payload) == {"result": True}


@pytest.mark.validation_result_creation
def test_perform_validation__ok(
    fake_document_type_repository: IDocumentTypeRepository,
    document_type_with_string_validator: DocumentType,
    perform_validation_message: CommandMessage,
    get_wrong_edata_request_mock,
    document_id,
    tenant_id,
):
    fake_document_type_repository.save(document_type_with_string_validator)

    result = perform_validation_handler(perform_validation_message)

    result_message: IMessage = result[FIRST_ELEMENT]
    assert result_message.get_header(ReplyMessageHeaders.REPLY_OUTCOME) == CommandReplyOutcome.SUCCESS.value
    assert json.loads(result_message.payload) == {"result": True}


@pytest.mark.validation_result_creation
def test_perform_validation__proxy_error__ok(
    fake_document_type_repository: IDocumentTypeRepository,
    document_type_with_string_validator: DocumentType,
    perform_validation_message: CommandMessage,
    error_get_edata_request_mock,
    document_id,
    tenant_id,
):
    fake_document_type_repository.save(document_type_with_string_validator)

    result = perform_validation_handler(perform_validation_message)

    result_message: IMessage = result[FIRST_ELEMENT]
    assert result_message.get_header(ReplyMessageHeaders.REPLY_OUTCOME) == CommandReplyOutcome.SUCCESS.value
    assert json.loads(result_message.payload) == {"result": False}


@pytest.mark.validation_result_creation
def test_perform_validation__internal_error__ok(
    fake_document_type_repository: IDocumentTypeRepository,
    document_type_with_string_validator: DocumentType,
    perform_validation_message: CommandMessage,
    get_right_edata_request_mock,
    document_id,
    tenant_id,
    mocker: MockerFixture,
):
    error_massage = "Something went wrong"
    mocker.patch.object(ExtractedDataValueUnit, "from_dict", side_effect=ValueError(error_massage))
    fake_document_type_repository.save(document_type_with_string_validator)

    result = perform_validation_handler(perform_validation_message)

    result_message: IMessage = result[FIRST_ELEMENT]
    assert result_message.get_header(ReplyMessageHeaders.REPLY_OUTCOME) == CommandReplyOutcome.SUCCESS.value
    assert json.loads(result_message.payload) == {"result": False}


@pytest.mark.validation_result_creation
def test_add_business_rule_violated_events__ok(
    fake_document_type_repository: IDocumentTypeRepository,
    document_type_with_string_validator_with_rule: DocumentType,
    domain_event_publisher: FakeDomainEventPublisher,
    perform_validation_message: CommandMessage,
    get_right_edata_request_mock,
    document_id,
    tenant_id,
):
    fake_document_type_repository.save(document_type_with_string_validator_with_rule)
    expected_events = [BusinessRuleViolated(document_id=document_id, field_code="string", message="Some error message")]

    result = perform_validation_handler(perform_validation_message)

    result_message: IMessage = result[FIRST_ELEMENT]
    published_events = domain_event_publisher.published
    assert result_message.get_header(ReplyMessageHeaders.REPLY_OUTCOME) == CommandReplyOutcome.SUCCESS.value
    assert json.loads(result_message.payload) == {"result": False}
    assert len(published_events) == 1
    assert published_events[FIRST_ELEMENT].events == expected_events


@pytest.mark.validation_result_creation
def test_perform_cross_field_validation__success(
    fake_document_type_repository: IDocumentTypeRepository,
    document_type: DocumentType,
    cross_field_validator: CrossFieldValidator,
    perform_validation_message: CommandMessage,
    get_right_edata_multi_string_fields_request_mock,
    document_id,
    tenant_id,
):
    document_type.add_string_validator(code="string").with_description().is_required().build()
    document_type.add_string_validator(code="string2").with_description().is_required().build()

    cross_field_validator.rule = "type_code__string == type_code__string2"
    cross_field_validator.validated_fields = [EntityCode("string"), EntityCode("string2")]
    document_type._cross_field_validators = {cross_field_validator.id(): cross_field_validator}
    fake_document_type_repository.save(document_type)

    result = perform_validation_handler(perform_validation_message)

    result_message: IMessage = result[FIRST_ELEMENT]
    assert result_message.get_header(ReplyMessageHeaders.REPLY_OUTCOME) == CommandReplyOutcome.SUCCESS.value

    payload = json.loads(result_message.payload)
    assert payload["result"] is True


@pytest.mark.validation_result_creation
def test_perform_cross_field_validation__validation_error(
    fake_document_type_repository: IDocumentTypeRepository,
    document_type: DocumentType,
    cross_field_validator: CrossFieldValidator,
    perform_validation_message: CommandMessage,
    get_right_edata_multi_string_fields_request_mock,
    document_id,
    tenant_id,
):
    document_type.add_string_validator(code="string").with_description().is_required().build()
    document_type.add_string_validator(code="string2").with_description().is_required().build()

    cross_field_validator.rule = "type_code__string != type_code__string2"
    cross_field_validator.validated_fields = [EntityCode("string"), EntityCode("string2")]
    document_type._cross_field_validators = {cross_field_validator.id(): cross_field_validator}
    fake_document_type_repository.save(document_type)

    result = perform_validation_handler(perform_validation_message)

    result_message: IMessage = result[FIRST_ELEMENT]
    assert result_message.get_header(ReplyMessageHeaders.REPLY_OUTCOME) == CommandReplyOutcome.SUCCESS.value

    payload = json.loads(result_message.payload)
    assert payload["result"] is False
