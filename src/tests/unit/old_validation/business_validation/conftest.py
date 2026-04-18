from copy import deepcopy

import pytest

from deps_high_sparrow.domain.model.document_type.validator.validation.dto.prepared_field import (
    Cell,
    Coordinates,
)
from deps_high_sparrow.domain.model.document_type.validator.validation.entities.constants import (
    Severity,
)
from deps_high_sparrow.domain.model.document_type.validator.validation.services.utils import (
    Message,
)

from ..factories.rule import RuleFactory


@pytest.fixture
def number_casted_field(casted_document_fields):
    return casted_document_fields[0]


@pytest.fixture
def rule_number(number_casted_field):
    return RuleFactory(
        field_code=number_casted_field.field_code,
        document_type_code=number_casted_field.document_type_code,
    )


@pytest.fixture
def two_rule_number(number_casted_field):
    return [
        RuleFactory(
            field_code=number_casted_field.field_code,
            document_type_code=number_casted_field.document_type_code,
        ),
        RuleFactory(
            field_code=number_casted_field.field_code,
            document_type_code=number_casted_field.document_type_code,
        ),
    ]


@pytest.fixture
def number_filed_name(number_casted_field):
    return f"{number_casted_field.document_type_code}__{number_casted_field.field_code}"


@pytest.fixture
def string_casted_field(casted_document_fields):
    return casted_document_fields[1]


@pytest.fixture
def rule_string(string_casted_field):
    return RuleFactory(
        field_code=string_casted_field.field_code,
        document_type_code=string_casted_field.document_type_code,
    )


@pytest.fixture
def string_filed_name(string_casted_field):
    return f"{string_casted_field.document_type_code}__{string_casted_field.field_code}"


@pytest.fixture
def table_casted_field(casted_document_fields):
    table = casted_document_fields[2]
    table.data.cells[1].value = 10
    return table


@pytest.fixture
def rule_table(table_casted_field):
    rule = RuleFactory(
        field_code=table_casted_field.field_code,
        document_type_code=table_casted_field.document_type_code,
    )
    return rule


@pytest.fixture
def table_filed_name(table_casted_field):
    return f"{table_casted_field.document_type_code}__{table_casted_field.field_code}"


@pytest.fixture
def table_issues(rule_table):
    return [
        Message(message=rule_table.issue_message, column=0, row=0),
        Message(message=rule_table.issue_message, column=1, row=0),
        Message(message="Table contains errors"),
    ]


@pytest.fixture
def list_of_severity_message_tuples():
    return [
        (Severity.ERROR, Message(message="message1")),
        (Severity.WARNING, Message(message="message2")),
    ]


@pytest.fixture
def dict_casted_field(casted_document_fields):
    return casted_document_fields[4]


@pytest.fixture
def rule_dict(dict_casted_field):
    rule = RuleFactory(
        field_code=dict_casted_field.field_code,
        document_type_code=dict_casted_field.document_type_code,
    )
    return rule


@pytest.fixture
def dict_filed_name(dict_casted_field):
    return f"{dict_casted_field.document_type_code}__{dict_casted_field.field_code}"


@pytest.fixture
def table_casted_field_multi_row(table_casted_field):
    table = deepcopy(table_casted_field)
    table.data.cells.extend(
        [
            Cell(value=2, coordinates=Coordinates(column=0, row=1)),
            Cell(value="other", coordinates=Coordinates(column=1, row=1)),
        ]
    )
    return table
