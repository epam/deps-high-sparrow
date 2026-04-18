from copy import deepcopy
from datetime import date

from deps_high_sparrow.domain.model.document_type.validator.validation.dto.field import (
    ArrayFieldTypeMeta,
    BasicFieldTypeMeta,
    DictFieldTypeMeta,
    StringFieldTypeMeta,
)
from deps_high_sparrow.domain.model.document_type.validator.validation.dto.prepared_field import (
    BaseData,
    BaseDataToValidate,
    Cell,
    Coordinates,
)
from deps_high_sparrow.domain.model.document_type.validator.validation.entities.constants import (
    OperandType,
)


def test_cast_number__pass(field_caster_service):
    assert field_caster_service.cast(value="1", field_type=OperandType.NUMBER) == 1


def test_cast_incorrect_type__(field_caster_service):
    assert isinstance(field_caster_service.cast(value=True, field_type=OperandType.BOOL), bool)


def test_cast_array__to_number__pass(field_caster_service, base_field_attributes):
    value = [
        BaseDataToValidate(
            **base_field_attributes,
            field_type=OperandType.NUMBER,
            data=BaseData(value="1"),
        ),
        BaseDataToValidate(
            **base_field_attributes,
            field_type=OperandType.NUMBER,
            data=BaseData(value=2),
        ),
        BaseDataToValidate(
            **base_field_attributes,
            field_type=OperandType.NUMBER,
            data=BaseData(value="3"),
        ),
    ]
    casted_fields = field_caster_service.cast(
        value=value,
        field_type=OperandType.ARRAY,
        meta=ArrayFieldTypeMeta(item_type=OperandType.NUMBER, meta=BasicFieldTypeMeta()),
    )
    assert [item.data.value for item in casted_fields] == [1, 2, 3]


def test_cast_table__pass(field_caster_service, prepared_table_field):
    cells = prepared_table_field.data.cells
    casted_table = field_caster_service.cast_table(cells, meta=prepared_table_field.meta)
    expected = [
        Cell(value=1.0, coordinates=Coordinates(column=0, row=0)),
        Cell(value=date(2000, 1, 1), coordinates=Coordinates(column=1, row=0)),
    ]
    assert casted_table == expected


def test_document_fields__pass(field_caster_service, prepared_document_fields, casted_document_fields):
    casted_fields = field_caster_service.cast_field_values(deepcopy(prepared_document_fields))
    assert casted_fields == casted_document_fields


def test_cast_dict_values__pass(field_caster_service, prepared_dict_field):
    casted_fields = field_caster_service.cast_dict(
        prepared_dict_field.data.items,
        field_type=OperandType.DICT,
        meta=DictFieldTypeMeta(
            key_type=OperandType.STRING,
            key_meta=StringFieldTypeMeta(),
            value_type=OperandType.DATE,
            value_meta=BasicFieldTypeMeta(),
        ),
    )

    assert casted_fields[0].data.value == "val"
    assert casted_fields[1].data.value == date(day=10, month=10, year=2020)
