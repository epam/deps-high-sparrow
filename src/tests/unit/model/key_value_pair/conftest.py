import pytest

from deps_high_sparrow.domain.model import DocumentArtifact


@pytest.fixture(scope="function")
def document_type(empty_document_type, entity_code_1, entity_code_2):
    # fmt: off
    empty_document_type.add_key_value_validator(entity_code_1) \
        .with_description() \
            .with_key() \
            .with_date_value() \
        .is_required() \
        .build()
    empty_document_type.add_key_value_validator(entity_code_2) \
        .with_description() \
            .with_key() \
            .with_date_value() \
        .build()
    # fmt: on
    return empty_document_type


@pytest.fixture
def prepared_key_value_artifact_1(entity_code_1):
    return DocumentArtifact(
        code=entity_code_1,
        value=("val", "10.10.2020"),
    )


@pytest.fixture
def prepared_key_value_artifact_2(entity_code_2):
    return DocumentArtifact(
        code=entity_code_2,
        value=("val", "10.10.2020"),
    )
