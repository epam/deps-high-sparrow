import pytest

from deps_high_sparrow.domain.model import DocumentArtifact


@pytest.fixture(scope="function")
def document_type(empty_document_type, entity_code_1):
    # fmt: off
    empty_document_type.add_table_validator(entity_code_1) \
        .with_description() \
            .for_number_column(index=0, is_required=True) \
            .for_date_column(index=1, is_required=False) \
            .for_number_column(index=2, is_required=False) \
            .for_number_column(index=0, is_required=True) \
            .for_date_column(index=1, is_required=False) \
            .for_number_column(index=2, is_required=False) \
        .is_required() \
        .build()
    # fmt: on
    return empty_document_type


@pytest.fixture
def prepared_table_artifact(entity_code_1):
    return DocumentArtifact(
        code=entity_code_1,
        value=[
            ["1", (0, 0)],
            ["01-01-2000", (1, 0)],
            ["10", (2, 0)],
            ["1", (0, 1)],
            ["01-01-2000", (1, 1)],
            ["10", (2, 1)],
        ],
    )
