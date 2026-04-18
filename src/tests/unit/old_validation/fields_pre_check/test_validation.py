from faker import Faker

from deps_high_sparrow.domain.model.document_type.validator.validation.dto.prepared_field import (
    TableDataToValidate,
)
from deps_high_sparrow.domain.model.document_type.validator.validation.services import (
    RequiredFieldsPreCheckService,
)
from deps_high_sparrow.domain.model.document_type.validator.validation.services.utils import (
    Message,
)

fake = Faker()


def test_validate__all_valid(
    required_prepared_field_not_none,
    valid_prepared_fields,
    fields_pre_check_service,
):
    validation_result = fields_pre_check_service.validate(valid_prepared_fields + required_prepared_field_not_none)
    assert validation_result.is_valid
    assert validation_result.detail == []


def test_validate__one_required_field_is_none(
    valid_prepared_fields,
    required_prepared_field_is_none,
    fields_pre_check_service,
):
    validation_result = fields_pre_check_service.validate(valid_prepared_fields + required_prepared_field_is_none)
    assert validation_result.is_valid is False
    assert validation_result.detail[0].errors == [Message(message="Field is required")]


def test_validate__optional_field_is_none(
    none_optional_prepared_field,
    fields_pre_check_service,
):
    validation_result = fields_pre_check_service.validate(none_optional_prepared_field)
    assert validation_result.is_valid


def test_validate__all_table_cell_valid(
    prepared_table_field,
    fields_pre_check_service,
):
    validation_result = fields_pre_check_service.validate([prepared_table_field])
    assert validation_result.is_valid


def test_validate__optional_cell_is_none(
    prepared_table_field,
    fields_pre_check_service,
    empty_value,
):
    prepared_table_field.data.cells[-1].value = empty_value
    validation_result = fields_pre_check_service.validate([prepared_table_field])
    assert validation_result.is_valid


def test_validate__required_cell_is_none(
    prepared_table_field,
    fields_pre_check_service,
    empty_value,
):
    prepared_table_field.data.cells[0].value = empty_value

    validation_result = fields_pre_check_service.validate([prepared_table_field])
    assert not validation_result.is_valid
    assert validation_result.detail[0].errors[0] == Message(message="Column is required", column=0, row=0)


def test_validate__list_of_tables__required_cell_is_none(
    prepared_array_of_tables_field,
    fields_pre_check_service,
):
    prepared_array_of_tables_field.data.items[0].data.cells[0].value = None

    validation_result = fields_pre_check_service.validate([prepared_array_of_tables_field])
    assert not validation_result.is_valid
    assert validation_result.detail[0].errors[0] == Message(message="Column is required", column=0, row=0, index=0)


def test_validate__required_table_is_empty(
    prepared_table_field,
    fields_pre_check_service,
):
    prepared_table_field.data.cells = []

    validation_result = fields_pre_check_service.validate([prepared_table_field])
    assert not validation_result.is_valid
    assert validation_result.detail[0].errors == [Message(message="Field is required")]


def test_validate__required_table_is_none(
    prepared_table_field,
    fields_pre_check_service,
):
    prepared_table_field.data = None

    validation_result = fields_pre_check_service.validate([prepared_table_field])
    assert not validation_result.is_valid
    assert validation_result.detail[0].errors == [Message(message="Field is required")]


def test_validate__cell_out_of_bounds(
    prepared_table_field: TableDataToValidate,
    fields_pre_check_service: RequiredFieldsPreCheckService,
):
    prepared_table_field.data.cells[-1].coordinates.column += 1

    validation_result = fields_pre_check_service.validate([prepared_table_field])
    assert not validation_result.is_valid
    assert validation_result.detail[0].errors == [Message(message=fields_pre_check_service.CELLS_OUT_OF_BOUNDS)]


def test_validate__required_dict_values_are_none(
    prepared_dict_field,
    fields_pre_check_service,
):
    expected_messages = {"Key is required", "Value is required"}
    for item in prepared_dict_field.data.items:
        item.data.value = None

    validation_result = fields_pre_check_service.validate([prepared_dict_field])
    messages = {msg.message for msg in validation_result.detail[0].errors}

    assert not validation_result.is_valid
    assert messages == expected_messages


def test_validate__optional_dict_values_are_none(
    prepared_dict_field,
    fields_pre_check_service,
):
    prepared_dict_field.is_required = False
    for item in prepared_dict_field.data.items:
        item.data.value = None

    validation_result = fields_pre_check_service.validate([prepared_dict_field])

    assert validation_result.is_valid
    assert validation_result.detail == []


def test_validate__required_array_of_dicts__item_is_none(prepared_array_of_dicts_field, fields_pre_check_service):
    expected_messages = {
        "Array contains errors",
        "Key is required",
        "Value is required",
    }

    for item in prepared_array_of_dicts_field.data.items[0].data.items:
        item.data.value = None

    validation_result = fields_pre_check_service.validate([prepared_array_of_dicts_field])
    messages = {msg.message for msg in validation_result.detail[0].errors}

    assert not validation_result.is_valid
    assert messages == expected_messages


def test_validate__required_array_of_dicts__item_exists(prepared_array_of_dicts_field, fields_pre_check_service):
    validation_result = fields_pre_check_service.validate([prepared_array_of_dicts_field])

    assert validation_result.is_valid
    assert validation_result.detail == []
