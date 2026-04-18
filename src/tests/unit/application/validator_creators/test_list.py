import pytest

from deps_high_sparrow.application import ListValidatorCreator
from deps_high_sparrow.domain.exceptions import BusinessException, ValidatorNotFound
from deps_high_sparrow.domain.model import (
    BasicDescription,
    DateDescription,
    EnumDescription,
    KeyValueDescription,
    ListDescription,
    OperandType,
    TableDescription,
)
from tests.data import (
    raw_date_list_field,
    raw_enum_list_field,
    raw_kvp_list_field,
    raw_list_field_without_field_constraint,
    raw_table_list_field,
    raw_table_list_field_with_wrong_item_type,
)

from .conftest import replaced_operand_types


@pytest.mark.validator_creation
def test_list__wrong_item_type__error(document_type):
    creator = ListValidatorCreator(document_type=document_type, raw_field=raw_table_list_field_with_wrong_item_type)

    with pytest.raises(BusinessException):
        creator.create()


@pytest.mark.validator_creation
def test_list__without_field_constraint__not_created(document_type):
    creator = ListValidatorCreator(document_type=document_type, raw_field=raw_list_field_without_field_constraint)

    creator.create()

    with pytest.raises(ValidatorNotFound):
        document_type.get_validator(raw_list_field_without_field_constraint["code"])


@pytest.mark.validator_creation
def test_list__basic_fields__ok(validator_creator, document_type, raw_basic_list_field):
    code = raw_basic_list_field["code"]

    validator_creator._create_list(raw_basic_list_field)

    validator = document_type.get_validator(code)
    item_type = raw_basic_list_field["field_data"]["base_type"]
    assert validator.code() == code
    assert validator.type_.type == OperandType.ARRAY
    assert validator.is_required == raw_basic_list_field["required"]
    assert isinstance(validator.type_.description, ListDescription)
    assert validator.type_.description.item_type == (
        item_type if item_type not in replaced_operand_types else replaced_operand_types[item_type]
    )
    assert isinstance(validator.type_.description.meta, BasicDescription)


@pytest.mark.validator_creation
def test_list__enum__ok(validator_creator, document_type):
    code = raw_enum_list_field["code"]

    validator_creator._create_list(raw_enum_list_field)

    validator = document_type.get_validator(code)
    expected_item_type = raw_enum_list_field["field_data"]["base_type"]
    expected_options = raw_enum_list_field["field_data"]["base_type_data"]["options"]
    assert validator.code() == code
    assert validator.type_.type == OperandType.ARRAY
    assert validator.is_required == raw_enum_list_field["required"]
    assert isinstance(validator.type_.description, ListDescription)
    assert validator.type_.description.item_type == expected_item_type
    assert isinstance(validator.type_.description.meta, EnumDescription)
    assert validator.type_.description.meta.options == expected_options


@pytest.mark.validator_creation
def test_list__date__ok(validator_creator, document_type):
    code = raw_date_list_field["code"]

    validator_creator._create_list(raw_date_list_field)

    validator = document_type.get_validator(code)
    expected_item_type = raw_date_list_field["field_data"]["base_type"]
    expected_format = raw_date_list_field["field_data"]["base_type_data"]["format"]
    assert validator.code() == code
    assert validator.type_.type == OperandType.ARRAY
    assert validator.is_required == raw_date_list_field["required"]
    assert isinstance(validator.type_.description, ListDescription)
    assert validator.type_.description.item_type == expected_item_type
    assert isinstance(validator.type_.description.meta, DateDescription)
    assert validator.type_.description.meta.format == expected_format


@pytest.mark.validator_creation
def test_list__table__ok(validator_creator, document_type):
    code = raw_table_list_field["code"]

    validator_creator._create_list(raw_table_list_field)

    raw_columns = raw_table_list_field["field_data"]["base_type_data"]["columns"]
    validator = document_type.get_validator(code)
    validator_columns = validator.type_.description.meta.columns
    expected_item_type = raw_table_list_field["field_data"]["base_type"]
    is_required = raw_table_list_field["required"]
    assert validator.code() == code
    assert validator.type_.type == OperandType.ARRAY
    assert validator.is_required == is_required
    assert isinstance(validator.type_.description, ListDescription)
    assert validator.type_.description.item_type == expected_item_type
    assert isinstance(validator.type_.description.meta, TableDescription)
    assert len(validator_columns) == len(raw_columns)

    for index, (raw_column, validator_column) in enumerate(zip(raw_columns, validator_columns)):
        column_type = raw_column["column_type"]

        assert validator_column.item_type == (
            column_type if column_type not in replaced_operand_types else replaced_operand_types[column_type]
        )
        assert validator_column.index == index
        assert validator_column.is_required == is_required


@pytest.mark.validator_creation
def test_list__key_value_pair__ok(validator_creator, document_type):
    code = raw_kvp_list_field["code"]

    validator_creator._create_list(raw_kvp_list_field)

    validator = document_type.get_validator(code)
    expected_item_type = raw_kvp_list_field["field_data"]["base_type"]
    assert validator.code() == code
    assert validator.type_.type == OperandType.ARRAY
    assert validator.is_required == raw_kvp_list_field["required"]
    assert isinstance(validator.type_.description, ListDescription)
    assert validator.type_.description.item_type == expected_item_type
    assert isinstance(validator.type_.description.meta, KeyValueDescription)
