from deps_high_sparrow.messaging.handlers import (
    extraction_field_modified_handler,
    extraction_field_modified_handler_for_corleone,
)


def test_extraction_field_created__ok(
    extraction_field_created_envelope,
    validator_service_mock,
    document_type_id,
    extraction_string_field,
    tenant_id,
):
    extraction_field_modified_handler(extraction_field_created_envelope)

    validator_service_mock.save_validator.assert_called_once_with(
        document_type_id,
        tenant_id=tenant_id,
        field=extraction_string_field,
    )


def test_extraction_field_updated__ok(
    extraction_field_updated_envelope,
    validator_service_mock,
    document_type_id,
    extraction_string_field,
    tenant_id,
):
    extraction_field_modified_handler(extraction_field_updated_envelope)

    validator_service_mock.save_validator.assert_called_once_with(
        document_type_id,
        tenant_id=tenant_id,
        field=extraction_string_field,
    )


def test_extraction_field_created_for_corleone__ok(
    extraction_field_created_envelope_for_corleone,
    validator_service_mock,
    document_type_id,
    extraction_string_field,
    tenant_id,
):
    extraction_field_modified_handler_for_corleone(extraction_field_created_envelope_for_corleone)

    validator_service_mock.save_validator.assert_called_once_with(
        document_type_id,
        tenant_id=tenant_id,
        field=extraction_string_field,
    )


def test_extraction_field_updated_for_corleone__ok(
    extraction_field_updated_envelope_for_corleone,
    validator_service_mock,
    document_type_id,
    extraction_string_field,
    tenant_id,
):
    extraction_field_modified_handler_for_corleone(extraction_field_updated_envelope_for_corleone)

    validator_service_mock.save_validator.assert_called_once_with(
        document_type_id,
        tenant_id=tenant_id,
        field=extraction_string_field,
    )
