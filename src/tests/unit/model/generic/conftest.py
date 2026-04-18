from uuid import uuid4

import pytest

from deps_high_sparrow.domain.model import DocumentArtifact


@pytest.fixture(scope="function")
def document_type(empty_document_type, entity_code_1, entity_code_2):
    # fmt: off
    empty_document_type.add_number_validator(entity_code_1) \
        .with_description() \
        .is_required() \
        .build()
    empty_document_type.add_string_validator(entity_code_2) \
        .with_description() \
        .is_required() \
        .build()
    # fmt: on
    return empty_document_type


@pytest.fixture
def prepared_artifact_1(entity_code_1):
    return DocumentArtifact(entity_code_1, "1")


@pytest.fixture
def prepared_artifact_2(entity_code_2):
    return DocumentArtifact(entity_code_2, uuid4().hex)


@pytest.fixture
def prepared_artifact_2_wrong_type_value(entity_code_2):
    return DocumentArtifact(entity_code_2, 5)
