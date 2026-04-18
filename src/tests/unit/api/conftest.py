import pytest
from faker import Faker

from deps_high_sparrow.api.serializers.v1 import CreateRuleRequest

fake = Faker()


@pytest.fixture
def create_rule_request(
    rule_name,
    rule_severity,
    rule_text,
    rule_issue_message,
    rule_description,
    rule_need_warning_even_if_optional,
    rule_for_each,
    rule_for_any,
    rule_check_optional_fields,
) -> CreateRuleRequest:
    return CreateRuleRequest(
        name=rule_name,
        severity=rule_severity,
        rule=rule_text,
        issue_message=rule_issue_message,
        description=rule_description,
        need_warning_even_if_optional=rule_need_warning_even_if_optional,
        for_each=rule_for_each,
        for_any=rule_for_any,
        check_optional_fields=rule_check_optional_fields,
    )
