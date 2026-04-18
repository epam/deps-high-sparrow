import pytest

from deps_high_sparrow.application import KVPValidatorCreator
from deps_high_sparrow.domain.exceptions import BusinessException
from deps_high_sparrow.domain.model import (
    BasicDescription,
    KeyValueDescription,
    OperandType,
)
from tests.data import raw_date_kvp_field_with_wrong_value_type


@pytest.mark.validator_creation
def test_key_value_pair__wrong_value_type__error(document_type):
    creator = KVPValidatorCreator(document_type=document_type, raw_field=raw_date_kvp_field_with_wrong_value_type)

    with pytest.raises(BusinessException):
        creator.create()


@pytest.mark.validator_creation
def test_key_value_pair__enum__ok(validator_creator, document_type, raw_enum_kvp_field):
    code = raw_enum_kvp_field["code"]

    validator_creator._create_dict(raw_enum_kvp_field)

    validator = document_type.get_validator(code)
    assert validator.code() == code
    assert validator.type_.type == OperandType.DICT
    assert validator.is_required == raw_enum_kvp_field["required"]
    assert validator.type_.description.value_type == raw_enum_kvp_field["field_data"]["value_type"]
    assert isinstance(validator.type_.description, KeyValueDescription)
    if raw_enum_kvp_field["field_data"].get("value_data"):
        assert (
            validator.type_.description.value_meta.options == raw_enum_kvp_field["field_data"]["value_data"]["options"]
        )
    else:
        isinstance(validator.type_.description.value_meta, BasicDescription)


@pytest.mark.validator_creation
def test_key_value_pair__date__ok(validator_creator, document_type, raw_date_kvp_field):
    code = raw_date_kvp_field["code"]

    validator_creator._create_dict(raw_date_kvp_field)

    validator = document_type.get_validator(code)
    assert validator.code() == code
    assert validator.type_.type == OperandType.DICT
    assert validator.is_required == raw_date_kvp_field["required"]
    assert validator.type_.description.value_type == raw_date_kvp_field["field_data"]["value_type"]
    assert isinstance(validator.type_.description, KeyValueDescription)
    if raw_date_kvp_field["field_data"].get("value_data"):
        assert validator.type_.description.value_meta.format == raw_date_kvp_field["field_data"]["value_data"]["format"]
    else:
        assert isinstance(validator.type_.description.value_meta, BasicDescription)
