def test_validator_string_builder(empty_document_type):
    # fmt: off
    empty_document_type \
        .add_string_validator("test_code") \
        .with_description() \
        .is_required() \
        .build()
    # fmt: on

    assert empty_document_type._validators != {}

    validator = empty_document_type.get_validator("test_code")

    assert validator.is_required
    assert "test_code" == validator.code()
    assert "string" == validator.type_.type.value


def test_validator_string_builder__without_description(empty_document_type):
    # fmt: off
    empty_document_type \
        .add_string_validator("test_code") \
        .is_required() \
        .build()
    # fmt: on

    assert empty_document_type._validators != {}

    validator = empty_document_type.get_validator("test_code")

    assert validator.is_required
    assert "test_code" == validator.code()
    assert "string" == validator.type_.type.value


def test_validator_key_value_builder__string_value(empty_document_type):
    # fmt: off
    empty_document_type \
        .add_key_value_validator("test_code") \
        .with_description() \
        .with_key() \
        .with_string_value() \
        .is_required() \
        .build()
    # fmt: on

    assert empty_document_type._validators != {}

    validator = empty_document_type.get_validator("test_code")

    assert validator.is_required
    assert "test_code" == validator.code()
    assert "dict" == validator.type_.type.value
    assert "string" == validator.type_.description.key_type.value
    assert "string" == validator.type_.description.value_type.value


def test_validator_key_value_builder__string_value__without_description(
    empty_document_type,
):
    # fmt: off
    empty_document_type \
        .add_key_value_validator("test_code") \
        .with_description() \
        .with_key() \
        .with_string_value() \
        .is_required() \
        .build()
    # fmt: on

    assert empty_document_type._validators != {}

    validator = empty_document_type.get_validator("test_code")

    assert validator.is_required
    assert "test_code" == validator.code()
    assert "dict" == validator.type_.type.value
    assert "string" == validator.type_.description.key_type.value
    assert "string" == validator.type_.description.value_type.value


def test_validator_key_value_builder__number_value(empty_document_type):
    # fmt: off
    empty_document_type \
        .add_key_value_validator("test_code") \
        .with_description() \
        .with_key() \
        .with_number_value() \
        .with_restrictions(allowed_values=["allow"], restricted_values=["deny"]) \
        .is_required() \
        .build()
    # fmt: on

    assert empty_document_type._validators != {}

    validator = empty_document_type.get_validator("test_code")

    assert validator.is_required
    assert "test_code" == validator.code()
    assert "dict" == validator.type_.type.value
    assert "string" == validator.type_.description.key_type.value
    assert "number" == validator.type_.description.value_type.value
    assert ["allow"] == validator.type_.description.value_meta.allowed_values
    assert ["deny"] == validator.type_.description.value_meta.restricted_values


def test_validator_key_value_builder__boolean_value(empty_document_type):
    # fmt: off
    empty_document_type \
        .add_key_value_validator("test_code") \
        .with_description() \
        .with_key() \
        .with_boolean_value() \
        .is_required() \
        .build()
    # fmt: on

    assert empty_document_type._validators != {}

    validator = empty_document_type.get_validator("test_code")

    assert validator.is_required
    assert "test_code" == validator.code()
    assert "dict" == validator.type_.type.value
    assert "string" == validator.type_.description.key_type.value
    assert "bool" == validator.type_.description.value_type.value


def test_validator_key_value_builder__range_value(empty_document_type):
    # fmt: off
    empty_document_type \
        .add_key_value_validator("test_code") \
        .with_description() \
        .with_key() \
        .with_range_value() \
        .is_required() \
        .build()
    # fmt: on

    assert empty_document_type._validators != {}

    validator = empty_document_type.get_validator("test_code")

    assert validator.is_required
    assert "test_code" == validator.code()
    assert "dict" == validator.type_.type.value
    assert "string" == validator.type_.description.key_type.value
    assert "range" == validator.type_.description.value_type.value


def test_validator_key_value_builder__date_value(empty_document_type):
    # fmt: off
    empty_document_type \
        .add_key_value_validator("test_code") \
        .with_description() \
        .with_key() \
        .with_date_value() \
        .with_format(format="format") \
        .is_required() \
        .build()
    # fmt: on

    assert empty_document_type._validators != {}

    validator = empty_document_type.get_validator("test_code")

    assert validator.is_required
    assert "test_code" == validator.code()
    assert "dict" == validator.type_.type.value
    assert "string" == validator.type_.description.key_type.value
    assert "date" == validator.type_.description.value_type.value
    assert "format" == validator.type_.description.value_meta.format


def test_validator_key_value_builder__time_value(empty_document_type):
    # fmt: off
    empty_document_type \
        .add_key_value_validator("test_code") \
        .with_description() \
        .with_key() \
        .with_time_value() \
        .is_required() \
        .build()
    # fmt: on

    assert empty_document_type._validators != {}

    validator = empty_document_type.get_validator("test_code")

    assert validator.is_required
    assert "test_code" == validator.code()
    assert "dict" == validator.type_.type.value
    assert "string" == validator.type_.description.key_type.value
    assert "time" == validator.type_.description.value_type.value


def test_validator_key_value_builder__datetime_value(empty_document_type):
    # fmt: off
    empty_document_type \
        .add_key_value_validator("test_code") \
        .with_description() \
        .with_key() \
        .with_datetime_value() \
        .is_required() \
        .build()
    # fmt: on

    assert empty_document_type._validators != {}

    validator = empty_document_type.get_validator("test_code")

    assert validator.is_required
    assert "test_code" == validator.code()
    assert "dict" == validator.type_.type.value
    assert "string" == validator.type_.description.key_type.value
    assert "datetime" == validator.type_.description.value_type.value


def test_validator_key_value_builder__enum_value(empty_document_type):
    # fmt: off
    empty_document_type \
        .add_key_value_validator("test_code") \
        .with_description() \
        .with_key() \
        .with_enum_value() \
        .with_options(options=["op1", "op2"]) \
        .is_required() \
        .build()
    # fmt: on

    assert empty_document_type._validators != {}

    validator = empty_document_type.get_validator("test_code")

    assert validator.is_required
    assert "test_code" == validator.code()
    assert "dict" == validator.type_.type.value
    assert "string" == validator.type_.description.key_type.value
    assert "enum" == validator.type_.description.value_type.value
    assert ["op1", "op2"] == validator.type_.description.value_meta.options


def test_validator_table_builder__string_column(empty_document_type):
    column_data = [
        (0, True),
        (1, False),
        (2, True),
        (3, False),
        (4, False),
        (5, True),
        (6, False),
    ]

    # fmt: off
    empty_document_type \
        .add_table_validator("test_code") \
        .with_description() \
        .for_string_column(*column_data[0]) \
        .for_number_column(*column_data[1]) \
        .for_boolean_column(*column_data[2]) \
        .for_range_column(*column_data[3]) \
        .for_date_column(*column_data[4]) \
        .with_format(format="format") \
        .for_time_column(*column_data[5]) \
        .for_enum_column(*column_data[6]) \
        .with_options(options=["op1", "op2"]) \
        .is_required() \
        .build()
    # fmt: on

    assert empty_document_type._validators != {}

    validator = empty_document_type.get_validator("test_code")

    assert validator.is_required
    assert "test_code" == validator.code()
    assert "table" == validator.type_.type.value

    assert 7 == len(validator.type_.description.columns)

    for i, column in enumerate(validator.type_.description.columns):
        index, is_required = column_data[i]

        assert index == column.index
        assert is_required == column.is_required

    assert "format" == validator.type_.description.columns[4].meta.format
    assert ["op1", "op2"] == validator.type_.description.columns[6].meta.options


def test_validator_list_builder__string_item(empty_document_type):
    # fmt: off
    empty_document_type \
        .add_list_validator("test_code") \
        .with_description() \
        .for_string_item() \
        .is_required() \
        .build()
    # fmt: on

    assert empty_document_type._validators != {}

    validator = empty_document_type.get_validator("test_code")

    assert validator.is_required
    assert "test_code" == validator.code()
    assert "array" == validator.type_.type.value
    assert "string" == validator.type_.description.item_type


def test_validator_list_builder__key_value_item(empty_document_type):
    # fmt: off
    empty_document_type \
        .add_list_validator("test_code") \
        .with_description() \
        .for_key_value_item() \
        .with_key() \
        .with_string_value() \
        .is_required() \
        .build()
    # fmt: on

    assert empty_document_type._validators != {}

    validator = empty_document_type.get_validator("test_code")

    assert validator.is_required
    assert "test_code" == validator.code()
    assert "array" == validator.type_.type.value
    assert "dict" == validator.type_.description.item_type


def test_validator_list_builder__table_item(empty_document_type):
    column_data = [
        (0, True),
        (1, False),
        (2, True),
        (3, False),
        (4, False),
        (5, True),
        (6, False),
    ]

    # fmt: off
    empty_document_type \
        .add_list_validator("test_code") \
        .with_description() \
        .for_table_item() \
            .for_string_column(*column_data[0]) \
            .for_number_column(*column_data[1]) \
            .for_boolean_column(*column_data[2]) \
            .for_range_column(*column_data[3]) \
            .for_date_column(*column_data[4]) \
                .with_format(format="format") \
            .for_time_column(*column_data[5]) \
            .for_enum_column(*column_data[6]) \
                .with_options(options=["op1", "op2"]) \
        .is_required() \
        .build()
    # fmt: on

    assert empty_document_type._validators != {}

    validator = empty_document_type.get_validator("test_code")

    assert validator.is_required
    assert "test_code" == validator.code()
    assert "array" == validator.type_.type.value
    assert "table" == validator.type_.description.item_type
