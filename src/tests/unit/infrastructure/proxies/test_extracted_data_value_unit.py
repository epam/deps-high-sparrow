# type: ignore
from typing import Any

import pytest

from deps_high_sparrow.domain import Value
from deps_high_sparrow.infrastructure.proxies import ExtractedDataValueUnit
from tests.data.extracted_data import (
    checkbox_field,
    enum_field,
    key_value_pair_field,
    list_checkbox_field,
    list_enum_field,
    list_key_value_pair_field,
    list_string_field,
    list_table_field,
    string_field,
    table_field,
)

FIRST_ELEMENT = 0


@pytest.mark.validation_result_creation
@pytest.mark.parametrize(
    "field,code,value",
    (
        (string_field, string_field["fieldCode"], string_field["data"]["value"]),
        (checkbox_field, checkbox_field["fieldCode"], checkbox_field["data"]["value"]),
        (enum_field, enum_field["fieldCode"], enum_field["data"]["value"]),
        (
            key_value_pair_field,
            key_value_pair_field["fieldCode"],
            (key_value_pair_field["data"]["key"]["value"], key_value_pair_field["data"]["value"]["value"]),
        ),
    ),
)
def test_from_dict__ok(field: dict[str, Any], code: str, value: Value):
    unit = ExtractedDataValueUnit.from_dict(field)

    assert unit.code == code
    assert unit.value == value


@pytest.mark.validation_result_creation
@pytest.mark.parametrize(
    "field,code,value",
    (
        (list_string_field, list_string_field["fieldCode"], [list_string_field["data"][FIRST_ELEMENT]["value"]]),
        (list_checkbox_field, list_checkbox_field["fieldCode"], [list_checkbox_field["data"][FIRST_ELEMENT]["value"]]),
        (list_enum_field, list_enum_field["fieldCode"], [list_enum_field["data"][FIRST_ELEMENT]["value"]]),
        (
            list_key_value_pair_field,
            list_key_value_pair_field["fieldCode"],
            [
                (
                    list_key_value_pair_field["data"][FIRST_ELEMENT]["key"]["value"],
                    list_key_value_pair_field["data"][FIRST_ELEMENT]["value"]["value"],
                ),
            ],
        ),
    ),
)
def test_from_dict__list_field__ok(field: dict[str, Any], code: str, value: Value):
    unit = ExtractedDataValueUnit.from_dict(field)

    assert unit.code == code
    assert unit.value == value


@pytest.mark.validation_result_creation
def test_from_dict__table_field__ok():
    expected_code = table_field["fieldCode"]
    expected_value = [
        (
            cell["value"],
            (cell["coordinates"]["column"], cell["coordinates"]["row"]),
        )
        for cell in table_field["data"]["cells"]
    ]

    unit = ExtractedDataValueUnit.from_dict(table_field)

    assert unit.code == expected_code
    assert unit.value == expected_value


@pytest.mark.validation_result_creation
def test_from_dict__list_table_field__ok():
    expected_code = list_table_field["fieldCode"]
    expected_value = [
        [
            (
                cell["value"],
                (cell["coordinates"]["column"], cell["coordinates"]["row"]),
            )
            for cell in list_table_field["data"][FIRST_ELEMENT]["cells"]
        ],
    ]

    unit = ExtractedDataValueUnit.from_dict(list_table_field)

    assert unit.code == expected_code
    assert unit.value == expected_value


@pytest.mark.validation_result_creation
def test_from_dict__wrong_field_data__error():
    with pytest.raises(ValueError):
        ExtractedDataValueUnit.from_dict({"data": {}})


@pytest.mark.validation_result_creation
def test_from_dict__empty_list_field_data__error():
    with pytest.raises(ValueError):
        ExtractedDataValueUnit.from_dict({"data": []})


@pytest.mark.validation_result_creation
def test_from_dict__wrong_list_field_data__error():
    with pytest.raises(ValueError):
        ExtractedDataValueUnit.from_dict({"data": [{}]})
