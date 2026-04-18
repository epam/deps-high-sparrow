import random
from copy import deepcopy
from datetime import date

import pytest

from deps_high_sparrow.domain.model.document_type.validator.validation.dto.field import (
    ArrayFieldTypeMeta,
    BasicFieldTypeMeta,
    ColumnTypeMeta,
    DictFieldTypeMeta,
    StringFieldTypeMeta,
    TableFieldTypeMeta,
)
from deps_high_sparrow.domain.model.document_type.validator.validation.dto.prepared_field import (
    ArrayData,
    ArrayDataToValidate,
    BaseData,
    Cell,
    Coordinates,
    DictData,
    DictDataToValidate,
    FieldDataToValidate,
    TableData,
    TableDataToValidate,
)
from deps_high_sparrow.domain.model.document_type.validator.validation.entities.constants import (
    OperandType,
)
from deps_high_sparrow.domain.model.document_type.validator.validation.services import (
    BusinessRulesValidationService,
    FieldCasterService,
    TypeValidationService,
)
from deps_high_sparrow.domain.model.document_type.validator.validation.services.fields_pre_check.validation import (
    RequiredFieldsPreCheckService,
)


@pytest.fixture
def document_id():
    return random.randint(1, 1000)


@pytest.fixture
def valid_prepared_fields(document_id):
    fields = [
        FieldDataToValidate(
            document_id=document_id,
            field_code="field_code1",
            document_type_code="document_type1",
            data=BaseData(value="1"),
            field_type=OperandType.NUMBER,
            meta=BasicFieldTypeMeta(),
        ),
        FieldDataToValidate(
            document_id=document_id,
            field_code="field_code2",
            document_type_code="document_type2",
            data=BaseData(value="val"),
            field_type=OperandType.STRING,
            meta=StringFieldTypeMeta(),
        ),
    ]
    yield fields


@pytest.fixture
def prepared_table_field(document_id):
    return TableDataToValidate(
        document_id=document_id,
        field_code="field_code3",
        document_type_code="document_type3",
        field_type=OperandType.TABLE,
        is_required=True,
        meta=TableFieldTypeMeta(
            columns=[
                ColumnTypeMeta(
                    index=0,
                    is_required=True,
                    item_type=OperandType.NUMBER,
                    meta=BasicFieldTypeMeta(),
                ),
                ColumnTypeMeta(
                    index=1,
                    is_required=False,
                    item_type=OperandType.DATE,
                    meta=BasicFieldTypeMeta(),
                ),
            ]
        ),
        data=TableData(
            cells=[
                Cell(value="1", coordinates=Coordinates(column=0, row=0)),
                Cell(value="01-01-2000", coordinates=Coordinates(column=1, row=0)),
            ]
        ),
    )


@pytest.fixture
def prepared_array_of_tables_field(document_id, prepared_table_field):
    table = deepcopy(prepared_table_field)
    table.field_code = f"item_of__field_code4"
    table.document_type_code = "document_type4"
    return ArrayDataToValidate(
        document_id=document_id,
        field_code="field_code4",
        document_type_code="document_type4",
        field_type=OperandType.ARRAY,
        is_required=True,
        meta=ArrayFieldTypeMeta(item_type=OperandType.TABLE, meta=table.meta),
        data=ArrayData(items=[table]),
    )


@pytest.fixture
def prepared_dict_field(document_id):
    return DictDataToValidate(
        document_id=document_id,
        field_code="field_code5",
        document_type_code="document_type5",
        data=DictData(
            items=(
                FieldDataToValidate(
                    document_id=document_id,
                    field_code="field_code5__0",
                    document_type_code="document_type5",
                    field_type=OperandType.STRING,
                    meta=StringFieldTypeMeta(),
                    data=BaseData(value="val"),
                ),
                FieldDataToValidate(
                    document_id=document_id,
                    field_code="field_code5__1",
                    document_type_code="document_type5",
                    field_type=OperandType.DATE,
                    meta=BasicFieldTypeMeta(),
                    data=BaseData(value="10.10.2020"),
                ),
            )
        ),
        field_type=OperandType.DICT,
        meta=DictFieldTypeMeta(
            key_type=OperandType.STRING,
            key_meta=StringFieldTypeMeta(),
            value_type=OperandType.DATE,
            value_meta=BasicFieldTypeMeta(),
        ),
    )


@pytest.fixture
def prepared_array_of_dicts_field(document_id, prepared_dict_field):
    dict = deepcopy(prepared_dict_field)
    dict.field_code = "item_of__field_code6"
    dict.data.items[0].field_code = "item_of__field_code6__0"
    dict.data.items[1].field_code = "item_of__field_code6__1"
    dict.document_type_code = dict.data.items[0].document_type_code = dict.data.items[
        1
    ].document_type_code = "document_type6"
    return ArrayDataToValidate(
        document_id=document_id,
        field_code="field_code6",
        document_type_code="document_type6",
        field_type=OperandType.ARRAY,
        is_required=True,
        meta=ArrayFieldTypeMeta(item_type=OperandType.DICT, meta=dict.meta),
        data=ArrayData(items=[dict]),
    )


@pytest.fixture
def prepared_document_fields(
    valid_prepared_fields,
    prepared_table_field,
    prepared_array_of_tables_field,
    prepared_dict_field,
    prepared_array_of_dicts_field,
):
    fields = [
        *valid_prepared_fields,
        prepared_table_field,
        prepared_array_of_tables_field,
        prepared_dict_field,
        prepared_array_of_dicts_field,
    ]
    yield fields


@pytest.fixture
def prepared_default_array_field(document_id):
    return ArrayDataToValidate(
        document_id=document_id,
        field_code="field_code5",
        document_type_code="document_type5",
        field_type=OperandType.ARRAY,
        is_required=True,
        meta=ArrayFieldTypeMeta(item_type=OperandType.NUMBER, meta=BasicFieldTypeMeta()),
        data=ArrayData(
            items=[
                FieldDataToValidate(
                    document_id=document_id,
                    field_code="item_of__field_code5",
                    document_type_code="document_type5",
                    field_type=OperandType.NUMBER,
                    meta=BasicFieldTypeMeta(),
                    data=BaseData(value="1"),
                )
            ]
        ),
    )


@pytest.fixture(params=(None, ""))
def empty_value(request):
    return request.param


@pytest.fixture
def mock_field_code():
    return "doc_type__field_name_1"


@pytest.fixture
def casted_document_fields(prepared_document_fields):
    fields = deepcopy(prepared_document_fields)
    fields[0].data.value = 1
    fields[1].data.value = "val"
    fields[2].data.cells[0].value = 1
    fields[2].data.cells[1].value = date(year=2000, month=1, day=1)
    fields[3].data.items[0].data.cells[0].value = 1
    fields[3].data.items[0].data.cells[1].value = date(year=2000, month=1, day=1)
    fields[4].data.items[0].data.value = "val"
    fields[4].data.items[1].data.value = date(year=2020, month=10, day=10)
    fields[5].data.items[0].data.items[0].data.value = "val"
    fields[5].data.items[0].data.items[1].data.value = date(year=2020, month=10, day=10)

    return fields


@pytest.fixture
def type_validation_service():
    return TypeValidationService()


@pytest.fixture
def fields_pre_check_service():
    return RequiredFieldsPreCheckService()


@pytest.fixture
def field_caster_service():
    return FieldCasterService()


@pytest.fixture
def business_validation_service():
    return BusinessRulesValidationService()
