import pytest

from deps_high_sparrow.messaging.handlers import get_document_types_reply_handler


@pytest.mark.document_type
def test_get_document_types__success__ok(
    get_document_types_success_reply_message,
    document_type_service_mock,
):
    document_type_service_mock.initialize_document_types.return_value = None

    get_document_types_reply_handler(get_document_types_success_reply_message)

    document_type_service_mock.initialize_document_types.assert_called_once_with(
        get_document_types_success_reply_message.command.document_types,
    )


@pytest.mark.document_type
def test_get_document_types__failed__no_error(
    get_document_types_failed_reply_message,
    document_type_service_mock,
):
    document_type_service_mock.initialize_document_types.return_value = None

    get_document_types_reply_handler(get_document_types_failed_reply_message)

    document_type_service_mock.initialize_document_types.assert_not_called()
