import pytest

from deps_high_sparrow.messaging.handlers import document_type_deleted_handler


@pytest.mark.document_type
def test_document_type_deleted__ok(
    document_type_deleted_envelope,
    document_type_service_mock,
    document_type_id,
    tenant_id,
):
    document_type_service_mock.delete_document_type.return_value = None

    document_type_deleted_handler(document_type_deleted_envelope)

    document_type_service_mock.delete_document_type.assert_called_once_with(
        document_type_id=document_type_id,
        tenant_id=tenant_id,
    )
