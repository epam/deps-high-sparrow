from uuid import uuid4

import pytest

from deps_high_sparrow.domain.model import DocumentType, RuleFieldReferencesValidator


@pytest.fixture
def document_id():
    return uuid4().hex


@pytest.fixture(params=(None, ""))
def empty_value(request):
    return request.param


@pytest.fixture(params=((None, None), (None, ""), ("", None), ("", "")))
def invalid_data_set_for_depended_rule(request):
    return request.param


@pytest.fixture(params=(("1", "1"), ("1", 0), (0, "1")))
def valid_data_set_for_depended_rule(request, invalid_data_set_for_depended_rule):
    depended_item, item_for_check = request.param
    return (
        depended_item if depended_item else invalid_data_set_for_depended_rule[0],
        item_for_check if item_for_check else invalid_data_set_for_depended_rule[1],
    )


@pytest.fixture(scope="function")
def empty_document_type(document_type_id, tenant_id):
    return DocumentType(document_type_id, tenant_id)


@pytest.fixture
def rule_field_references_validator():
    return RuleFieldReferencesValidator()
