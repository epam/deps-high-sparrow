import random

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
)
from tests.unit.old_validation.factories.rule import RuleFactory


@pytest.fixture
def document_id():
    return random.randint(1, 1000)


@pytest.fixture
def business_validation_service():
    return BusinessRulesValidationService()


@pytest.fixture
def array_field_with_multiple_items(document_id):
    return ArrayDataToValidate(
        document_id=document_id,
        field_code="array_field",
        document_type_code="doc_type",
        field_type=OperandType.ARRAY,
        is_required=True,
        meta=ArrayFieldTypeMeta(item_type=OperandType.NUMBER, meta=BasicFieldTypeMeta()),
        data=ArrayData(
            items=[
                FieldDataToValidate(
                    document_id=document_id,
                    field_code="item_of__array_field",
                    document_type_code="doc_type",
                    field_type=OperandType.NUMBER,
                    meta=BasicFieldTypeMeta(),
                    data=BaseData(value=10),
                ),
                FieldDataToValidate(
                    document_id=document_id,
                    field_code="item_of__array_field",
                    document_type_code="doc_type",
                    field_type=OperandType.NUMBER,
                    meta=BasicFieldTypeMeta(),
                    data=BaseData(value=20),
                ),
                FieldDataToValidate(
                    document_id=document_id,
                    field_code="item_of__array_field",
                    document_type_code="doc_type",
                    field_type=OperandType.NUMBER,
                    meta=BasicFieldTypeMeta(),
                    data=BaseData(value=30),
                ),
            ]
        ),
    )


@pytest.fixture
def rule_object_factory():
    def _build_rule(field_code, document_type_code):
        return RuleFactory(
            field_code=field_code,
            document_type_code=document_type_code,
        )

    return _build_rule


@pytest.fixture
def array_of_dicts_with_multiple_items(document_id):
    dict_item_1 = DictDataToValidate(
        document_id=document_id,
        field_code="item_of__array_dicts",
        document_type_code="doc_type",
        data=DictData(
            items=(
                FieldDataToValidate(
                    document_id=document_id,
                    field_code="item_of__array_dicts__0",
                    document_type_code="doc_type",
                    field_type=OperandType.STRING,
                    meta=StringFieldTypeMeta(),
                    data=BaseData(value="key1"),
                ),
                FieldDataToValidate(
                    document_id=document_id,
                    field_code="item_of__array_dicts__1",
                    document_type_code="doc_type",
                    field_type=OperandType.STRING,
                    meta=StringFieldTypeMeta(),
                    data=BaseData(value="value1"),
                ),
            )
        ),
        field_type=OperandType.DICT,
        meta=DictFieldTypeMeta(
            key_type=OperandType.STRING,
            key_meta=StringFieldTypeMeta(),
            value_type=OperandType.STRING,
            value_meta=StringFieldTypeMeta(),
        ),
    )

    dict_item_2 = DictDataToValidate(
        document_id=document_id,
        field_code="item_of__array_dicts",
        document_type_code="doc_type",
        data=DictData(
            items=(
                FieldDataToValidate(
                    document_id=document_id,
                    field_code="item_of__array_dicts__0",
                    document_type_code="doc_type",
                    field_type=OperandType.STRING,
                    meta=StringFieldTypeMeta(),
                    data=BaseData(value="key2"),
                ),
                FieldDataToValidate(
                    document_id=document_id,
                    field_code="item_of__array_dicts__1",
                    document_type_code="doc_type",
                    field_type=OperandType.STRING,
                    meta=StringFieldTypeMeta(),
                    data=BaseData(value="value2"),
                ),
            )
        ),
        field_type=OperandType.DICT,
        meta=DictFieldTypeMeta(
            key_type=OperandType.STRING,
            key_meta=StringFieldTypeMeta(),
            value_type=OperandType.STRING,
            value_meta=StringFieldTypeMeta(),
        ),
    )

    return ArrayDataToValidate(
        document_id=document_id,
        field_code="array_dicts",
        document_type_code="doc_type",
        field_type=OperandType.ARRAY,
        is_required=True,
        meta=ArrayFieldTypeMeta(item_type=OperandType.DICT, meta=dict_item_1.meta),
        data=ArrayData(items=[dict_item_1, dict_item_2]),
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
def table_field(document_id):
    return TableDataToValidate(
        document_id=document_id,
        field_code="table_1",
        document_type_code="doc_type",
        field_type=OperandType.TABLE,
        is_required=True,
        meta=TableFieldTypeMeta(
            columns=[
                ColumnTypeMeta(
                    index=0,
                    is_required=True,
                    item_type=OperandType.STRING,
                    meta=StringFieldTypeMeta(),
                ),
                ColumnTypeMeta(
                    index=1,
                    is_required=False,
                    item_type=OperandType.STRING,
                    meta=StringFieldTypeMeta(),
                ),
            ]
        ),
        data=TableData(
            cells=[
                Cell(value="data", coordinates=Coordinates(column=0, row=0)),
                Cell(value="value1", coordinates=Coordinates(column=1, row=0)),
                Cell(value="", coordinates=Coordinates(column=0, row=1)),
                Cell(value="value2", coordinates=Coordinates(column=1, row=1)),
                Cell(value="data3", coordinates=Coordinates(column=0, row=2)),
                Cell(value="", coordinates=Coordinates(column=1, row=2)),
                Cell(value="8", coordinates=Coordinates(column=0, row=3)),
                Cell(value="9", coordinates=Coordinates(column=1, row=3)),
            ]
        ),
    )
