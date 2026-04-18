from uuid import uuid4

__all__ = [
    "string_field",
    "list_string_field",
    "with_string_field",
    "enum_field",
    "list_enum_field",
    "key_value_pair_field",
    "list_key_value_pair_field",
    "table_field",
    "list_table_field",
    "checkbox_field",
    "list_checkbox_field",
]

string_field = {"data": {"value": uuid4().hex}, "fieldCode": "string"}

list_string_field = {"data": [{"value": uuid4().hex}], "fieldCode": "list_string"}

checkbox_field = {"data": {"value": True}, "fieldCode": "checkbox"}

list_checkbox_field = {"data": [{"value": True}], "fieldCode": "list_checkbox"}

enum_field = {"data": {"value": uuid4().hex}, "fieldCode": "enum"}

list_enum_field = {"data": [{"value": uuid4().hex}], "fieldCode": "list_enum"}

key_value_pair_field = {
    "data": {
        "key": {"value": uuid4().hex},
        "value": {"value": False},
    },
    "fieldCode": "kv_pair_1",
}

list_key_value_pair_field = {
    "data": [
        {
            "key": {"value": uuid4().hex},
            "value": {"value": False},
        },
    ],
    "fieldCode": "kv_pair_1",
}

table_field = {
    "data": {
        "cells": [
            {
                "coordinates": {"colspan": 1, "column": 0, "row": 0, "rowspan": 1},
                "value": uuid4().hex,
            },
            {
                "coordinates": {"colspan": 1, "column": 1, "row": 0, "rowspan": 1},
                "value": uuid4().hex,
            },
            {
                "coordinates": {"colspan": 1, "column": 0, "row": 1, "rowspan": 1},
                "value": uuid4().hex,
            },
            {
                "coordinates": {"colspan": 1, "column": 1, "row": 1, "rowspan": 1},
                "value": uuid4().hex,
            },
        ],
    },
    "fieldCode": "table",
}

list_table_field = {
    "data": [
        {
            "cells": [
                {
                    "coordinates": {"colspan": 1, "column": 0, "row": 0, "rowspan": 1},
                    "value": uuid4().hex,
                },
                {
                    "coordinates": {"colspan": 1, "column": 1, "row": 0, "rowspan": 1},
                    "value": uuid4().hex,
                },
                {
                    "coordinates": {"colspan": 1, "column": 0, "row": 1, "rowspan": 1},
                    "value": uuid4().hex,
                },
                {
                    "coordinates": {"colspan": 1, "column": 1, "row": 1, "rowspan": 1},
                    "value": uuid4().hex,
                },
            ],
        },
    ],
    "fieldCode": "table",
}

with_string_field = {"documentId": 537, "fields": [string_field]}
