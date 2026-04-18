import pytest

from deps_high_sparrow.application import TableValidatorCreator
from deps_high_sparrow.domain.exceptions import BusinessException
from deps_high_sparrow.domain.model import TableDescription
from tests.data import raw_table_field2, raw_table_field_wrong_field_types

from .conftest import replaced_operand_types


@pytest.mark.validator_creation
def test_table__with_field_constraint__ok(validator_creator, document_type):
    creator = TableValidatorCreator(document_type=document_type, raw_field=raw_table_field2)

    creator.create()

    validator = document_type.get_validator(raw_table_field2["code"])
    validator_columns = validator.type_.description.columns
    raw_columns = raw_table_field2["field_data"]["columns"]
    assert isinstance(validator.type_.description, TableDescription)
    assert len(validator_columns) == len(raw_columns)

    for index, (raw_column, validator_column) in enumerate(zip(raw_columns, validator_columns)):
        column_type = raw_column["column_type"]

        assert validator_column.item_type == (
            column_type if column_type not in replaced_operand_types else replaced_operand_types[column_type]
        )
        assert validator_column.index == index
        assert validator_column.is_required == raw_table_field2["required"]


@pytest.mark.validator_creation
def test_table__wrong_column_type__error(document_type):
    creator = TableValidatorCreator(document_type=document_type, raw_field=raw_table_field_wrong_field_types)

    with pytest.raises(BusinessException):
        creator.create()
