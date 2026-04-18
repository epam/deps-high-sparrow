from copy import deepcopy
from http import HTTPStatus
from random import randint
from typing import Any

import pytest
import requests_mock
from deps_message_flow.commands.consumer import CommandMessage

from deps_high_sparrow.domain import DocumentType, Severity
from tests.data.extracted_data import string_field, with_string_field

FIRST_ELEMENT = 0


@pytest.fixture
def document_id() -> str:
    return str(randint(1, 9999))


@pytest.fixture
def edata_with_string_field(document_id) -> dict[str, Any]:
    edata = deepcopy(with_string_field)
    edata["documentId"] = document_id

    return edata


@pytest.fixture
def edata_with_string_fields(document_id) -> dict[str, Any]:
    edata = deepcopy(with_string_field)
    edata["fields"].append(
        {"data": {"value": string_field["data"]["value"]}, "fieldCode": "string2"},  # type: ignore[index]
    )
    edata["documentId"] = document_id

    return edata


@pytest.fixture
def edata_with_wrong_string_field(edata_with_string_field) -> dict[str, Any]:
    edata = deepcopy(edata_with_string_field)
    edata["fields"][FIRST_ELEMENT]["data"]["value"] = "*" * (1000 + 1)

    return edata


@pytest.fixture
def get_right_edata_request_mock(document_id, extraction_proxy, edata_with_string_field):
    with requests_mock.Mocker() as m:
        m.register_uri(
            url=f"{extraction_proxy._base_url}{extraction_proxy.v2_url_suffix}/extracted-data/{document_id}",
            method="GET",
            json=edata_with_string_field,
        )
        yield m


@pytest.fixture
def get_right_edata_multi_string_fields_request_mock(document_id, extraction_proxy, edata_with_string_fields):
    with requests_mock.Mocker() as m:
        m.register_uri(
            url=f"{extraction_proxy._base_url}{extraction_proxy.v2_url_suffix}/extracted-data/{document_id}",
            method="GET",
            json=edata_with_string_fields,
        )
        yield m


@pytest.fixture
def get_wrong_edata_request_mock(document_id, extraction_proxy, edata_with_wrong_string_field):
    with requests_mock.Mocker() as m:
        m.register_uri(
            url=f"{extraction_proxy._base_url}{extraction_proxy.v2_url_suffix}/extracted-data/{document_id}",
            method="GET",
            json=edata_with_wrong_string_field,
        )
        yield m


@pytest.fixture
def error_get_edata_request_mock(document_id, extraction_proxy, edata_with_wrong_string_field):
    with requests_mock.Mocker() as m:
        m.register_uri(
            url=f"{extraction_proxy._base_url}{extraction_proxy.v2_url_suffix}/extracted-data/{document_id}",
            method="GET",
            status_code=HTTPStatus.BAD_REQUEST,
            json={"code": "bad request"},
        )
        yield m


@pytest.fixture
def perform_validation_message(mocker, document_id, document_type) -> CommandMessage:
    cm = mocker.Mock()
    cm.command.document_id = document_id
    cm.command.document_type_id = document_type.id()

    return cm


@pytest.fixture
def document_type_with_string_validator(document_type) -> DocumentType:
    new_document_type = deepcopy(document_type)
    (new_document_type.add_string_validator(code="string").with_description().is_required().build())

    return new_document_type


@pytest.fixture
def document_type_with_string_validator_with_rule(document_type_with_string_validator) -> DocumentType:
    new_document_type = deepcopy(document_type_with_string_validator)
    new_document_type.validators[FIRST_ELEMENT].add_rule(
        name="Rule name",
        severity=Severity.ERROR,
        rule=f"type_code__string == 1",
        issue_message="Some error message",
    )

    return new_document_type
