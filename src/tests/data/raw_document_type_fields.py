from random import randint
from uuid import uuid4

from deps_high_sparrow.application import FieldType
from deps_high_sparrow.domain import OperandType

from .char_type import CharType

__all__ = [
    "raw_string_field1",
    "raw_string_field2",
    "raw_number_field1",
    "raw_number_field2",
    "raw_checkmark_field1",
    "raw_checkmark_field2",
    "raw_range_field1",
    "raw_range_field2",
    "raw_time_field1",
    "raw_time_field2",
    "raw_datetime_field1",
    "raw_datetime_field2",
    "raw_date_field1",
    "raw_date_field2",
    "raw_enum_field1",
    "raw_enum_field2",
    "raw_table_field1",
    "raw_table_field2",
    "raw_string_list_field",
    "raw_enum_list_field",
    "raw_date_list_field",
    "raw_table_list_field",
    "raw_enum_kvp_field1",
    "raw_enum_kvp_field2",
    "raw_date_kvp_field1",
    "raw_date_kvp_field2",
    "raw_kvp_list_field",
    "raw_table_field_wrong_field_types",
    "raw_date_kvp_field_with_wrong_value_type",
    "raw_table_list_field_with_wrong_item_type",
    "raw_list_field_without_field_constraint",
]

columns = [
    {
        "column_data": {"char_blacklist": "r", "char_type": CharType.ALPHABETIC.value, "char_whitelist": "r"},
        "column_type": FieldType.STRING.value,
        "title": uuid4().hex,
    },
    {
        "column_data": {"char_type": CharType.NUMERIC.value},
        "column_type": OperandType.NUMBER.value,
        "title": uuid4().hex,
    },
    {
        "column_data": {"char_type": CharType.BOOLEAN.value},
        "column_type": FieldType.CHECKMARK.value,
        "title": uuid4().hex,
    },
    {
        "column_data": None,
        "column_type": OperandType.RANGE.value,
        "title": uuid4().hex,
    },
    {
        "column_data": {"format": "%d/%m/%Y"},
        "column_type": FieldType.DATE.value,
        "title": uuid4().hex,
    },
    {
        "column_data": None,
        "column_type": OperandType.TIME.value,
        "title": uuid4().hex,
    },
    {
        "column_data": None,
        "column_type": OperandType.DATETIME.value,
        "title": uuid4().hex,
    },
    {
        "column_data": {"options": ["test", "test1"]},
        "column_type": FieldType.ENUM.value,
        "title": uuid4().hex,
    },
]

raw_string_field1 = {
    "code": uuid4().hex,
    "document_type_id": uuid4().hex,
    "field_data": {"char_blacklist": "j", "char_whitelist": "d"},
    "field_type": FieldType.STRING.value,
    "id": uuid4().hex,
    "name": uuid4().hex,
    "order": randint(1, 100),
    "required": True,
}

raw_string_field2 = {
    "code": uuid4().hex,
    "document_type_id": uuid4().hex,
    "field_data": None,
    "field_type": FieldType.STRING.value,
    "id": uuid4().hex,
    "name": uuid4().hex,
    "order": randint(1, 100),
    "required": False,
}

raw_number_field1 = {
    "code": uuid4().hex,
    "document_type_id": uuid4().hex,
    "field_data": {"char_type": CharType.NUMERIC.value},
    "field_type": OperandType.NUMBER.value,
    "id": uuid4().hex,
    "name": uuid4().hex,
    "order": randint(1, 100),
    "required": True,
}

raw_number_field2 = {
    "code": uuid4().hex,
    "document_type_id": uuid4().hex,
    "field_data": None,
    "field_type": OperandType.NUMBER.value,
    "id": uuid4().hex,
    "name": uuid4().hex,
    "order": randint(1, 100),
    "required": False,
}

raw_checkmark_field1 = {
    "code": uuid4().hex,
    "document_type_id": uuid4().hex,
    "field_data": {"char_type": CharType.BOOLEAN.value},
    "field_type": FieldType.CHECKMARK.value,
    "id": uuid4().hex,
    "name": uuid4().hex,
    "order": randint(1, 100),
    "required": True,
}

raw_checkmark_field2 = {
    "code": uuid4().hex,
    "document_type_id": uuid4().hex,
    "field_data": None,
    "field_type": FieldType.CHECKMARK.value,
    "id": uuid4().hex,
    "name": uuid4().hex,
    "order": randint(1, 100),
    "required": False,
}

raw_range_field1 = {
    "code": uuid4().hex,
    "document_type_id": uuid4().hex,
    "field_data": None,
    "field_type": OperandType.RANGE.value,
    "id": uuid4().hex,
    "name": uuid4().hex,
    "order": randint(1, 100),
    "required": True,
}

raw_range_field2 = {
    "code": uuid4().hex,
    "document_type_id": uuid4().hex,
    "field_data": None,
    "field_type": OperandType.RANGE.value,
    "id": uuid4().hex,
    "name": uuid4().hex,
    "order": randint(1, 100),
    "required": False,
}

raw_time_field1 = {
    "code": uuid4().hex,
    "document_type_id": uuid4().hex,
    "field_data": None,
    "field_type": OperandType.TIME.value,
    "id": uuid4().hex,
    "name": uuid4().hex,
    "order": randint(1, 100),
    "required": True,
}

raw_time_field2 = {
    "code": uuid4().hex,
    "document_type_id": uuid4().hex,
    "field_data": None,
    "field_type": OperandType.TIME.value,
    "id": uuid4().hex,
    "name": uuid4().hex,
    "order": randint(1, 100),
    "required": False,
}

raw_datetime_field1 = {
    "code": uuid4().hex,
    "document_type_id": uuid4().hex,
    "field_data": None,
    "field_type": OperandType.DATETIME.value,
    "id": uuid4().hex,
    "name": uuid4().hex,
    "order": randint(1, 100),
    "required": True,
}

raw_datetime_field2 = {
    "code": uuid4().hex,
    "document_type_id": uuid4().hex,
    "field_data": None,
    "field_type": OperandType.DATETIME.value,
    "id": uuid4().hex,
    "name": uuid4().hex,
    "order": randint(1, 100),
    "required": False,
}

raw_date_field1 = {
    "code": uuid4().hex,
    "document_type_id": uuid4().hex,
    "field_data": {"format": "%d/%m/%Y"},
    "field_type": FieldType.DATE.value,
    "id": uuid4().hex,
    "name": uuid4().hex,
    "order": randint(1, 100),
    "required": True,
}

raw_date_field2 = {
    "code": uuid4().hex,
    "document_type_id": uuid4().hex,
    "field_data": None,
    "field_type": FieldType.DATE.value,
    "id": uuid4().hex,
    "name": uuid4().hex,
    "order": randint(1, 100),
    "required": False,
}

raw_enum_field1 = {
    "code": uuid4().hex,
    "document_type_id": uuid4().hex,
    "field_data": {"options": ["test", "test1"]},
    "field_type": FieldType.ENUM.value,
    "id": uuid4().hex,
    "name": uuid4().hex,
    "order": randint(1, 100),
    "required": True,
}

raw_enum_field2 = {
    "code": uuid4().hex,
    "document_type_id": uuid4().hex,
    "field_data": None,
    "field_type": FieldType.ENUM.value,
    "id": uuid4().hex,
    "name": uuid4().hex,
    "order": randint(1, 100),
    "required": False,
}

raw_table_field1 = {
    "code": uuid4().hex,
    "document_type_id": uuid4().hex,
    "field_data": None,
    "field_type": FieldType.TABLE.value,
    "id": uuid4().hex,
    "name": uuid4().hex,
    "order": randint(1, 100),
    "required": False,
}

raw_table_field_wrong_field_types = {
    "code": uuid4().hex,
    "document_type_id": uuid4().hex,
    "field_data": {
        "columns": [
            {
                "column_data": None,
                "column_type": "wrong_field_type",
                "title": uuid4().hex,
            },
        ],
    },
    "field_type": "wrong_field_type",
    "id": uuid4().hex,
    "name": uuid4().hex,
    "order": randint(1, 100),
    "required": False,
}

raw_table_field2 = {
    "code": uuid4().hex,
    "document_type_id": uuid4().hex,
    "field_data": {"columns": columns},
    "field_type": FieldType.TABLE.value,
    "id": uuid4().hex,
    "name": uuid4().hex,
    "order": randint(1, 100),
    "required": True,
}

raw_string_list_field = {
    "code": uuid4().hex,
    "document_type_id": uuid4().hex,
    "field_data": {
        "base_type": OperandType.STRING.value,
        "base_type_data": {
            "char_blacklist": "125",
            "char_type": CharType.ALPHABETIC.value,
            "char_whitelist": None,
        },
    },
    "field_type": FieldType.LIST.value,
    "id": uuid4().hex,
    "name": uuid4().hex,
    "order": randint(1, 100),
    "required": True,
}

raw_enum_list_field = {
    "code": uuid4().hex,
    "document_type_id": uuid4().hex,
    "field_data": {
        "base_type": OperandType.ENUM.value,
        "base_type_data": {"options": ["f", "n", "m"]},
    },
    "field_type": FieldType.LIST.value,
    "id": uuid4().hex,
    "name": uuid4().hex,
    "order": randint(1, 100),
    "required": True,
}

raw_date_list_field = {
    "code": uuid4().hex,
    "document_type_id": uuid4().hex,
    "field_data": {
        "base_type": OperandType.DATE.value,
        "base_type_data": {"format": "%d/%m/%Y"},
    },
    "field_type": FieldType.LIST.value,
    "id": uuid4().hex,
    "name": uuid4().hex,
    "order": randint(1, 100),
    "required": True,
}

raw_table_list_field = {
    "code": uuid4().hex,
    "document_type_id": uuid4().hex,
    "field_data": {
        "base_type": OperandType.TABLE.value,
        "base_type_data": {"columns": columns},
    },
    "field_type": FieldType.LIST.value,
    "id": uuid4().hex,
    "name": uuid4().hex,
    "order": randint(1, 100),
    "required": True,
}

raw_kvp_list_field = {
    "code": uuid4().hex,
    "document_type_id": uuid4().hex,
    "field_data": {
        "base_type": OperandType.DICT.value,
        "base_type_data": {
            "key_data": None,
            "key_type": FieldType.STRING.value,
            "value_data": None,
            "value_type": FieldType.STRING.value,
        },
    },
    "field_type": FieldType.LIST.value,
    "id": uuid4().hex,
    "name": uuid4().hex,
    "order": randint(1, 100),
    "required": True,
}

raw_table_list_field_with_wrong_item_type = {
    "code": uuid4().hex,
    "document_type_id": uuid4().hex,
    "field_data": {
        "base_type": "wrong_item_type",
        "base_type_data": {"columns": columns},
    },
    "field_type": FieldType.LIST.value,
    "id": uuid4().hex,
    "name": uuid4().hex,
    "order": randint(1, 100),
    "required": True,
}

raw_list_field_without_field_constraint = {
    "code": uuid4().hex,
    "document_type_id": uuid4().hex,
    "field_data": None,
    "field_type": FieldType.LIST.value,
    "id": uuid4().hex,
    "name": uuid4().hex,
    "order": randint(1, 100),
    "required": True,
}

raw_enum_kvp_field1 = {
    "code": uuid4().hex,
    "document_type_id": uuid4().hex,
    "field_data": {
        "key_data": None,
        "key_type": FieldType.STRING.value,
        "value_data": {"options": ["test", "test1"]},
        "value_type": FieldType.ENUM.value,
    },
    "field_type": FieldType.DICT.value,
    "id": uuid4().hex,
    "name": uuid4().hex,
    "order": randint(1, 100),
    "required": True,
}

raw_enum_kvp_field2 = {
    "code": uuid4().hex,
    "document_type_id": uuid4().hex,
    "field_data": {
        "key_data": None,
        "key_type": FieldType.STRING.value,
        "value_data": None,
        "value_type": FieldType.ENUM.value,
    },
    "field_type": FieldType.DICT.value,
    "id": uuid4().hex,
    "name": uuid4().hex,
    "order": randint(1, 100),
    "required": False,
}

raw_date_kvp_field1 = {
    "code": uuid4().hex,
    "document_type_id": uuid4().hex,
    "field_data": {
        "key_data": None,
        "key_type": FieldType.STRING.value,
        "value_data": {"format": "%d/%m/%Y"},
        "value_type": FieldType.DATE.value,
    },
    "field_type": FieldType.DICT.value,
    "id": uuid4().hex,
    "name": uuid4().hex,
    "order": randint(1, 100),
    "required": True,
}

raw_date_kvp_field2 = {
    "code": uuid4().hex,
    "document_type_id": uuid4().hex,
    "field_data": {
        "key_data": None,
        "key_type": FieldType.STRING.value,
        "value_data": None,
        "value_type": FieldType.DATE.value,
    },
    "field_type": FieldType.DICT.value,
    "id": uuid4().hex,
    "name": uuid4().hex,
    "order": randint(1, 100),
    "required": False,
}

raw_date_kvp_field_with_wrong_value_type = {
    "code": uuid4().hex,
    "document_type_id": uuid4().hex,
    "field_data": {
        "key_data": None,
        "key_type": FieldType.STRING.value,
        "value_data": None,
        "value_type": "wrong_value_type",
    },
    "field_type": FieldType.DICT.value,
    "id": uuid4().hex,
    "name": uuid4().hex,
    "order": randint(1, 100),
    "required": False,
}
