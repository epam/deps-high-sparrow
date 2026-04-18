from random import randint
from uuid import uuid4

import pytest

from deps_high_sparrow.application import FieldType, ValidatorCreator
from deps_high_sparrow.domain import OperandType
from tests.data import (
    raw_checkmark_field1,
    raw_checkmark_field2,
    raw_date_field1,
    raw_date_field2,
    raw_date_kvp_field1,
    raw_date_kvp_field2,
    raw_datetime_field1,
    raw_datetime_field2,
    raw_enum_field1,
    raw_enum_field2,
    raw_enum_kvp_field1,
    raw_enum_kvp_field2,
    raw_number_field1,
    raw_number_field2,
    raw_range_field1,
    raw_range_field2,
    raw_string_field1,
    raw_string_field2,
    raw_time_field1,
    raw_time_field2,
)

__all__ = ["replaced_operand_types"]

replaced_operand_types = {
    FieldType.CHECKMARK: OperandType.BOOL,
    FieldType.LIST: OperandType.ARRAY,
}


@pytest.fixture
def validator_creator(document_type) -> ValidatorCreator:
    return ValidatorCreator(document_type)


@pytest.fixture(params=[raw_string_field1, raw_string_field2])
def raw_string_field(request):
    return request.param


@pytest.fixture(params=[raw_date_field1, raw_date_field2])
def raw_date_field(request):
    return request.param


@pytest.fixture(params=[raw_enum_field1, raw_enum_field2])
def raw_enum_field(request):
    return request.param


@pytest.fixture(params=[raw_checkmark_field1, raw_checkmark_field2])
def raw_checkmark_field(request):
    return request.param


@pytest.fixture(
    params=[
        OperandType.NUMBER.value,
        FieldType.CHECKMARK.value,
        OperandType.RANGE.value,
        OperandType.TIME.value,
        OperandType.DATETIME.value,
    ],
)
def raw_basic_list_field(request):
    return {
        "code": uuid4().hex,
        "document_type_id": uuid4().hex,
        "field_data": {"base_type": request.param},
        "field_type": FieldType.LIST.value,
        "id": uuid4().hex,
        "name": uuid4().hex,
        "order": randint(1, 100),
        "required": True,
    }


@pytest.fixture(
    params=[
        OperandType.NUMBER.value,
        FieldType.CHECKMARK.value,
        OperandType.RANGE.value,
        OperandType.TIME.value,
        OperandType.DATETIME.value,
    ],
)
def raw_basic_kvp_field(request):
    item_type = request.param
    return {
        "code": uuid4().hex,
        "document_type_id": uuid4().hex,
        "field_data": {
            "key_data": None,
            "key_type": item_type,
            "value_data": None,
            "value_type": item_type,
        },
        "field_type": FieldType.DICT.value,
        "id": uuid4().hex,
        "name": uuid4().hex,
        "order": randint(1, 100),
        "required": True,
    }


@pytest.fixture(
    params=[
        raw_enum_kvp_field1,
        raw_enum_kvp_field2,
    ],
)
def raw_enum_kvp_field(request):
    return request.param


@pytest.fixture(
    params=[
        raw_date_kvp_field1,
        raw_date_kvp_field2,
    ],
)
def raw_date_kvp_field(request):
    return request.param


@pytest.fixture(
    params=[
        raw_number_field1,
        raw_number_field2,
        raw_range_field1,
        raw_range_field2,
        raw_time_field1,
        raw_time_field2,
        raw_datetime_field1,
        raw_datetime_field2,
    ],
)
def raw_basic_field(request):
    return request.param
