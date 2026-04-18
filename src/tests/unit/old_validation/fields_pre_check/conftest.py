import pytest
from faker import Faker

from deps_high_sparrow.domain.model.document_type.validator.validation.dto.field import (
    BasicFieldTypeMeta,
)
from deps_high_sparrow.domain.model.document_type.validator.validation.dto.prepared_field import (
    BaseData,
    FieldDataToValidate,
)
from deps_high_sparrow.domain.model.document_type.validator.validation.entities.constants import (
    OperandType,
)

fake = Faker()


@pytest.fixture
def required_prepared_field_not_none():
    return [
        FieldDataToValidate(
            document_id=fake.pyint(),
            field_code="field_code3",
            document_type_code="document_type3",
            data=BaseData(value=fake.pyint()),
            field_type=OperandType.NUMBER,
            meta=BasicFieldTypeMeta(),
        ),
    ]


@pytest.fixture
def required_prepared_field_is_none():
    return [
        FieldDataToValidate(
            document_id=fake.pyint(),
            field_code="field_code3",
            document_type_code="document_type3",
            data=BaseData(value=None),
            field_type=OperandType.NUMBER,
            meta=BasicFieldTypeMeta(),
        ),
    ]


@pytest.fixture
def none_optional_prepared_field():
    return [
        FieldDataToValidate(
            document_id=fake.pyint(),
            field_code="field_code3",
            document_type_code="document_type3",
            data=BaseData(value=None),
            field_type=OperandType.NUMBER,
            meta=BasicFieldTypeMeta(),
            is_required=False,
        ),
    ]
