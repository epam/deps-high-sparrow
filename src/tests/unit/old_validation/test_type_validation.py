from datetime import datetime

import pytest

from deps_high_sparrow.domain.model.document_type.validator.validation.dto.field import (
    BasicFieldTypeMeta,
    DateFieldTypeMeta,
    EnumFieldTypeMeta,
    StringFieldTypeMeta,
)
from deps_high_sparrow.domain.model.document_type.validator.validation.entities.constants import (
    KeyValueId,
    OperandType,
)
from deps_high_sparrow.domain.model.document_type.validator.validation.exceptions import (
    InvalidType,
)
from deps_high_sparrow.domain.model.document_type.validator.validation.services.type_validation.constants import (
    DATE_FORMATS,
)
from deps_high_sparrow.domain.model.document_type.validator.validation.services.utils import (
    Message,
)

INVALID_DATE_FORMAT_MESSAGE = "Invalid type: Field is not a date or invalid date format"
FIELD_NOT_NUMBER_MESSAGE = "Invalid type: Field is not a number"


def test_with_valid_values(
    type_validation_service,
    prepared_document_fields,
):
    validation_result = type_validation_service.validate(prepared_document_fields)
    assert validation_result.is_valid


def test_with_invalid_values(
    type_validation_service,
    prepared_document_fields,
):
    prepared_document_fields[1].field_type = OperandType.NUMBER
    validation_result = type_validation_service.validate(prepared_document_fields)
    assert not validation_result.is_valid


def test_table_validation_with_valid_cells(type_validation_service, prepared_table_field):
    result = type_validation_service.validate_table(prepared_table_field)
    assert not result.errors


def test_table_validation_with_invalid_cell(type_validation_service, prepared_table_field):
    prepared_table_field.data.cells[0].value = "not a number"
    result = type_validation_service.validate_table(prepared_table_field)
    assert result.errors[0].message == FIELD_NOT_NUMBER_MESSAGE


def test_table_validation_with_invalid_optional_cell(type_validation_service, prepared_table_field):
    prepared_table_field.data.cells[1].value = "not a date"
    result = type_validation_service.validate_table(prepared_table_field)
    assert result.errors[0].message == INVALID_DATE_FORMAT_MESSAGE


def test_table_validation_with_empty_optional_cell(type_validation_service, prepared_table_field, empty_value):
    prepared_table_field.data.cells[1].value = empty_value
    result = type_validation_service.validate_table(prepared_table_field)
    assert not result.errors


def test_number_validation__valid_value__pass(type_validation_service):
    check_value = 1.5
    assert type_validation_service._validate_number(check_value, BasicFieldTypeMeta()) == check_value


def test_number_validation__in_allowed_values__pass(type_validation_service):
    check_value = 1.5
    assert (
        type_validation_service._validate_number(check_value, BasicFieldTypeMeta(allowed_values=[check_value, 2]))
        == check_value
    )


def test_number_validation__invalid_value__raise_error(type_validation_service):
    with pytest.raises(InvalidType) as exp:
        type_validation_service._validate_number("not a number", BasicFieldTypeMeta())
    assert FIELD_NOT_NUMBER_MESSAGE == exp.value.msg


def test_number_validation__in_allowed_list__raise_error(type_validation_service):
    restricted_values = [1]
    with pytest.raises(InvalidType) as exp:
        type_validation_service._validate_number(1, BasicFieldTypeMeta(restricted_values=restricted_values))
    assert f"Invalid type: Field value should not be from {restricted_values}" == exp.value.msg


def test_number_validation__not_in_allowed_list__raise_error(type_validation_service):
    allowed_list = [2, 3]
    with pytest.raises(InvalidType) as exp:
        type_validation_service._validate_number(1, BasicFieldTypeMeta(allowed_values=allowed_list))
    assert f"Invalid type: Field value should be from {allowed_list}" == exp.value.msg


def test_bool_validation__correct_value__pass(type_validation_service):
    assert type_validation_service._validate_boolean(True, BasicFieldTypeMeta())
    assert not type_validation_service._validate_boolean(False, BasicFieldTypeMeta())


def test_bool_validation__invalide_value__raise_error(type_validation_service):
    with pytest.raises(InvalidType) as exp:
        type_validation_service._validate_boolean("not a bool", BasicFieldTypeMeta())
    assert "Invalid type: Field is not a bool" == exp.value.msg


def test_string_validation__string_value__pass(type_validation_service):
    value = "string"
    assert type_validation_service._validate_string(value, StringFieldTypeMeta()) == value


def test_string_validation__none_value__raise_error(type_validation_service):
    with pytest.raises(InvalidType) as exp:
        type_validation_service._validate_string(None, StringFieldTypeMeta())
    assert "Invalid type: Field is not a string" == exp.value.msg


def test_string_validation_german_symblos__pass(type_validation_service):
    german_string = "Märkischer Promenade 1a Blankenfelde"
    assert type_validation_service._validate_string(german_string, StringFieldTypeMeta()) == german_string


def test_date_with_format_validation__correct_value__pass(type_validation_service):
    date_string = "02/28/15"
    meta = DateFieldTypeMeta("%m/%d/%y")
    assert type_validation_service._validate_date(date_string, meta) == datetime.strptime(date_string, meta.format)


def test_date_with_format_validation__not_a_date__raise_error(type_validation_service):
    with pytest.raises(InvalidType) as exp:
        type_validation_service._validate_date("not a date", DateFieldTypeMeta(format="%d.%m.%y"))
    assert INVALID_DATE_FORMAT_MESSAGE == exp.value.msg


def test_date_validation__correct_value__pass(type_validation_service):
    date_string = "01.05.2010"
    assert type_validation_service._validate_date(date_string, BasicFieldTypeMeta()) == datetime.strptime(
        date_string, DATE_FORMATS[0]
    )


def test_date_validation__not_a_date__raise_error(type_validation_service):
    with pytest.raises(InvalidType) as exp:
        type_validation_service._validate_date("not a date", BasicFieldTypeMeta())
    assert INVALID_DATE_FORMAT_MESSAGE == exp.value.msg


def test_date_validation__invalid_date_format__raise_error(type_validation_service):
    with pytest.raises(InvalidType) as exp:
        type_validation_service._validate_date("2010^05^01", BasicFieldTypeMeta())
    assert INVALID_DATE_FORMAT_MESSAGE == exp.value.msg


def test_enum_validation__value_in_list__pass(type_validation_service):
    check_value = "value1"
    enum_values = [check_value, "value2"]
    assert type_validation_service._validate_enum(check_value, EnumFieldTypeMeta(options=enum_values)) == check_value


def test_enum_validation__value_not_from_range__raise_error(type_validation_service):
    check_value = "value1"
    enum_values = ["value2"]

    with pytest.raises(InvalidType) as exp:
        type_validation_service._validate_enum(check_value, EnumFieldTypeMeta(options=enum_values))
    options = ", ".join(f"'{option}'" for option in enum_values)
    assert f"Invalid type: Field value should be one of the following options: {options}" == exp.value.msg


def test_table_array_validation__table_type__pass(type_validation_service, prepared_array_of_tables_field):
    assert type_validation_service.validate_array(prepared_array_of_tables_field).errors == []


def test_table_array_validation___table_type_fail(type_validation_service, prepared_array_of_tables_field):
    prepared_array_of_tables_field.data.items[0].data.cells[0].value = "Not number"
    result = type_validation_service.validate_array(prepared_array_of_tables_field)
    assert result.errors
    assert result.errors[0] == Message(message="Invalid type: Field is not a number", column=0, row=0, index=0)


def test_number_array_validation__number_type__pass(type_validation_service, prepared_default_array_field):
    assert not type_validation_service.validate_array(prepared_default_array_field).errors


def test_number_array_validation__string_type__pass(type_validation_service, prepared_default_array_field):
    prepared_default_array_field.meta.item_type = OperandType.STRING
    prepared_default_array_field.data.items[0].field_type = OperandType.STRING
    prepared_default_array_field.data.items[0].meta = StringFieldTypeMeta()
    prepared_default_array_field.data.items[0].data.value = "?123#"

    assert not type_validation_service.validate_array(prepared_default_array_field).errors


def test_number_array__invalid_number(type_validation_service, prepared_default_array_field):
    prepared_default_array_field.data.items[0].data.value = "?123#"
    assert type_validation_service.validate_array(prepared_default_array_field).errors[0] == Message(
        message=FIELD_NOT_NUMBER_MESSAGE, index=0
    )


def test_array_validation__no_a_list__raise_error(type_validation_service, prepared_default_array_field):
    prepared_default_array_field.data.items = None
    msg = type_validation_service.validate_array(prepared_default_array_field).errors[0]
    assert Message(message="Invalid type: Field value is not an array") == msg


def test_dict_validation__correct_value__pass(type_validation_service, prepared_dict_field):
    assert not type_validation_service.validate_dict(prepared_dict_field).errors


def test_array_of_dicts_validation__correct_dict_value__pass(type_validation_service, prepared_array_of_dicts_field):
    assert not type_validation_service.validate_array(prepared_array_of_dicts_field).errors
