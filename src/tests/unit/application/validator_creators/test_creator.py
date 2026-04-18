import pytest

from deps_high_sparrow.domain.exceptions import BusinessException
from deps_high_sparrow.domain.model import (
    BasicDescription,
    DateDescription,
    EnumDescription,
    KeyValueDescription,
    ListDescription,
    OperandType,
    StringDescription,
    TableDescription,
)
from tests.data import (
    raw_string_list_field,
    raw_table_field1,
    raw_table_field_wrong_field_types,
)

from .conftest import replaced_operand_types


@pytest.mark.validator_creation
def test__create_for_field__wrong_type__error(validator_creator):
    with pytest.raises(BusinessException):
        validator_creator.create_for_field(raw_table_field_wrong_field_types)


@pytest.mark.validator_creation
def test__create_for_fields__wrong_type__error(validator_creator):
    with pytest.raises(BusinessException):
        validator_creator.create_for_fields([raw_table_field_wrong_field_types])


@pytest.mark.validator_creation
def test_basic__ok(validator_creator, document_type, raw_basic_field):
    code = raw_basic_field["code"]

    validator_creator._create_basic(raw_basic_field)

    validator = document_type.get_validator(code)
    assert validator.code() == code
    assert validator.type_.type == raw_basic_field["field_type"]
    assert isinstance(validator.type_.description, BasicDescription)
    assert validator.is_required == raw_basic_field["required"]


@pytest.mark.validator_creation
def test_string__ok(validator_creator, document_type, raw_string_field):
    code = raw_string_field["code"]

    validator_creator._create_string(raw_string_field)

    validator = document_type.get_validator(code)
    assert validator.code() == code
    assert validator.type_.type == raw_string_field["field_type"]
    assert isinstance(validator.type_.description, StringDescription)
    assert validator.is_required == raw_string_field["required"]


@pytest.mark.validator_creation
def test_date__ok(validator_creator, document_type, raw_date_field):
    code = raw_date_field["code"]

    validator_creator._create_date(raw_date_field)

    validator = document_type.get_validator(code)
    assert validator.code() == code
    assert validator.type_.type == raw_date_field["field_type"]
    assert validator.is_required == raw_date_field["required"]

    if raw_field_constraint := raw_date_field.get("field_data"):
        assert isinstance(validator.type_.description, DateDescription)
        assert validator.type_.description.format == raw_field_constraint["format"]
    else:
        assert isinstance(validator.type_.description, BasicDescription)


@pytest.mark.validator_creation
def test_enum__ok(validator_creator, document_type, raw_enum_field):
    code = raw_enum_field["code"]

    validator_creator._create_enum(raw_enum_field)

    validator = document_type.get_validator(code)
    assert validator.code() == code
    assert validator.type_.type == raw_enum_field["field_type"]
    assert validator.is_required == raw_enum_field["required"]

    if raw_field_constraint := raw_enum_field.get("field_data"):
        assert isinstance(validator.type_.description, EnumDescription)
        assert validator.type_.description.options == raw_field_constraint["options"]
    else:
        assert isinstance(validator.type_.description, BasicDescription)


@pytest.mark.validator_creation
def test_checkmark__ok(validator_creator, document_type, raw_checkmark_field):
    code = raw_checkmark_field["code"]

    validator_creator._create_basic(raw_checkmark_field)

    validator = document_type.get_validator(code)
    assert validator.code() == code
    assert validator.type_.type == OperandType.BOOL
    assert isinstance(validator.type_.description, BasicDescription)
    assert validator.is_required == raw_checkmark_field["required"]


@pytest.mark.validator_creation
def test_table__ok(validator_creator, document_type):
    code = raw_table_field1["code"]

    validator_creator._create_table(raw_table_field1)

    validator = document_type.get_validator(code)
    assert validator.code() == code
    assert validator.type_.type == raw_table_field1["field_type"]
    assert validator.is_required == raw_table_field1["required"]
    assert isinstance(validator.type_.description, TableDescription)
    assert validator.type_.description.columns == []


@pytest.mark.validator_creation
def test_list__ok(validator_creator, document_type):
    code = raw_string_list_field["code"]

    validator_creator._create_list(raw_string_list_field)

    validator = document_type.get_validator(code)
    assert validator.code() == code
    assert validator.type_.type == OperandType.ARRAY
    assert validator.is_required == raw_string_list_field["required"]
    assert isinstance(validator.type_.description, ListDescription)
    assert validator.type_.description.item_type == raw_string_list_field["field_data"]["base_type"]
    assert isinstance(validator.type_.description.meta, StringDescription)


@pytest.mark.validator_creation
def test_key_value_pair__ok(validator_creator, document_type, raw_basic_kvp_field):
    code = raw_basic_kvp_field["code"]

    validator_creator._create_dict(raw_basic_kvp_field)

    validator = document_type.get_validator(code)
    value_type = raw_basic_kvp_field["field_data"]["value_type"]
    assert validator.code() == code
    assert validator.type_.type == OperandType.DICT
    assert validator.is_required == raw_basic_kvp_field["required"]
    assert isinstance(validator.type_.description, KeyValueDescription)
    assert validator.type_.description.value_type == (
        value_type if value_type not in replaced_operand_types else replaced_operand_types[value_type]
    )
