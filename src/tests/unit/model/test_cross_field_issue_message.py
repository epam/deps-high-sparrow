from deps_high_sparrow.domain.model.shared import EntityCode
from deps_high_sparrow.domain.model.validation_result import CrossFieldIssueMessage


def test_cross_field_issue_message_creation__valid_parameters__succeeds(
    cross_field_issue_message_text, cross_field_dependent_fields
):
    issue_message = CrossFieldIssueMessage(
        message=cross_field_issue_message_text,
        dependent_fields=cross_field_dependent_fields,
    )

    assert issue_message.message == cross_field_issue_message_text
    assert issue_message.dependent_fields == cross_field_dependent_fields


def test_cross_field_issue_message_equality__same_values__equal():
    message1 = CrossFieldIssueMessage(
        message="test message",
        dependent_fields=[EntityCode("field1"), EntityCode("field2")],
    )
    message2 = CrossFieldIssueMessage(
        message="test message",
        dependent_fields=[EntityCode("field1"), EntityCode("field2")],
    )

    assert message1 == message2


def test_cross_field_issue_message_equality__different_values__not_equal():
    message1 = CrossFieldIssueMessage(
        message="test message",
        dependent_fields=[EntityCode("field1"), EntityCode("field2")],
    )
    message2 = CrossFieldIssueMessage(
        message="different message",
        dependent_fields=[EntityCode("field3")],
    )

    assert message1 != message2
