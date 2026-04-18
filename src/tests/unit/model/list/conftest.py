import pytest

from deps_high_sparrow.domain.model import DocumentArtifact


@pytest.fixture(scope="function")
def document_type(empty_document_type, entity_code_1, entity_code_2, entity_code_3, entity_code_4):
    # fmt: off
    empty_document_type.add_list_validator(entity_code_1) \
        .with_description() \
            .for_key_value_item() \
                .with_key() \
                .with_date_value() \
        .is_required() \
        .build()
    empty_document_type.add_list_validator(entity_code_2) \
        .with_description() \
            .for_table_item() \
                .for_number_column(index=0, is_required=True) \
                .for_date_column(index=1, is_required=False) \
                .for_number_column(index=2, is_required=False) \
                .for_number_column(index=0, is_required=True) \
                .for_date_column(index=1, is_required=False) \
                .for_number_column(index=2, is_required=False) \
        .is_required() \
        .build()
    empty_document_type.add_list_validator(entity_code_3) \
        .with_description() \
            .for_number_item() \
        .is_required() \
        .build()
    empty_document_type.add_list_validator(entity_code_4) \
        .with_description() \
            .for_string_item() \
        .is_required() \
        .build()
    # fmt: on
    return empty_document_type


@pytest.fixture
def prepared_key_value_list_artifact(entity_code_1):
    return DocumentArtifact(
        code=entity_code_1,
        value=[
            ["val", "10.10.2020"],
        ],
    )


@pytest.fixture
def prepared_table_list_artifact(entity_code_2):
    return DocumentArtifact(
        code=entity_code_2,
        value=[
            [
                ["1", (0, 0)],
                ["01-01-2000", (1, 0)],
                ["10", (2, 0)],
                ["1", (0, 1)],
                ["01-01-2000", (1, 1)],
                ["10", (2, 1)],
            ],
        ],
    )


@pytest.fixture
def prepared_number_list_artifact(entity_code_3):
    return DocumentArtifact(
        code=entity_code_3,
        value=["5"],
    )


@pytest.fixture
def prepared_string_list_artifact(entity_code_4):
    return DocumentArtifact(
        code=entity_code_4,
        value=["5"],
    )
