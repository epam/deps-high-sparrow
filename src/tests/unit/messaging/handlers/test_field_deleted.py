from deps_high_sparrow.messaging.handlers import (
    extraction_field_deleted_handler,
    extraction_field_deleted_handler_for_corleone,
)


def test_extraction_field_deleted_for_corleone__ok(
    extraction_field_deleted_envelope_for_corleone,
    validator_service_mock,
    document_type_id,
    extraction_field_code,
    tenant_id,
):
    extraction_field_deleted_handler_for_corleone(extraction_field_deleted_envelope_for_corleone)

    validator_service_mock.remove_validator.assert_called_once_with(
        document_type_id,
        tenant_id=tenant_id,
        field_code=extraction_field_code,
    )


def test_extraction_field_deleted__ok(
    extraction_field_deleted_envelope,
    validator_service_mock,
    document_type_id,
    extraction_field_code,
    tenant_id,
):
    extraction_field_deleted_handler(extraction_field_deleted_envelope)

    validator_service_mock.remove_validator.assert_called_once_with(
        document_type_id,
        tenant_id=tenant_id,
        field_code=extraction_field_code,
    )
