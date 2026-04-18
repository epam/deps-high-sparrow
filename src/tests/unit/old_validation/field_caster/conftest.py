from copy import deepcopy
from datetime import date

import pytest
from faker import Faker

from deps_high_sparrow.domain.model.document_type.validator.validation.dto.field import (
    BasicFieldTypeMeta,
)

fake = Faker()


@pytest.fixture
def base_field_attributes(document_id):
    return dict(
        document_id=document_id,
        field_code=fake.pystr(),
        document_type_code=fake.pystr(),
        meta=BasicFieldTypeMeta(),
        is_required=True,
    )
