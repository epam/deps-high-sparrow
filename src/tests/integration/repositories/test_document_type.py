from uuid import uuid4

from deps_high_sparrow.domain.model import (
    CrossFieldIssueMessage,
    DocumentType,
    EntityCode,
    Severity,
)


def test_save__new_document_type__ok(document_type_repository, document_type):
    document_type_repository.save(document_type)

    saved_document_type = document_type_repository.document_type_of_id(document_type.id(), document_type.tenant_id())

    assert document_type == saved_document_type


def test_save__new_document_type_with_validator_and_rule__ok(
    document_type_repository, document_type_with_string_validator_and_one_rule
):
    document_type_repository.save(document_type_with_string_validator_and_one_rule)

    saved_document_type = document_type_repository.document_type_of_id(
        document_type_with_string_validator_and_one_rule.id(),
        document_type_with_string_validator_and_one_rule.tenant_id(),
    )

    assert document_type_with_string_validator_and_one_rule == saved_document_type


def test_document_type_of_id__doc_type_exists__return_doc_type(document_type_repository, document_type):
    document_type_repository.save(document_type)
    saved_document_type = document_type_repository.document_type_of_id(document_type.id(), document_type.tenant_id())

    assert document_type == saved_document_type


def test_document_type_of_id__doc_type_not_exists__return_none(document_type_repository, document_type):
    saved_document_type = document_type_repository.document_type_of_id(document_type.id(), document_type.tenant_id())

    assert saved_document_type is None


def test_delete__doc_type_exists__doc_type_deleted(document_type_repository, document_type):
    document_type_repository.save(document_type)
    document_type_repository.delete(document_type.id(), document_type.tenant_id())
    deleted_document_type = document_type_repository.document_type_of_id(document_type.id(), document_type.tenant_id())

    assert deleted_document_type is None


def test_delete__doc_type_not_exists(document_type_repository, document_type):
    document_type_repository.delete(document_type.id(), document_type.tenant_id())
    deleted_document_type = document_type_repository.document_type_of_id(document_type.id(), document_type.tenant_id())

    assert deleted_document_type is None


def test_save__doc_type_exists__rule_added__doc_type_updated(
    document_type_repository, document_type_with_string_validator_and_one_rule, validator_code
):
    document_type_repository.save(document_type_with_string_validator_and_one_rule)

    validator = document_type_with_string_validator_and_one_rule.get_validator(code=validator_code)
    new_rule_name = "new rule"
    validator.add_rule(
        name=new_rule_name,
        severity=Severity.ERROR,
        rule="test rule",
        issue_message="test rule",
    )

    document_type_repository.save(document_type_with_string_validator_and_one_rule)

    updated_document_type = document_type_repository.document_type_of_id(
        document_type_with_string_validator_and_one_rule.id(),
        document_type_with_string_validator_and_one_rule.tenant_id(),
    )
    updated_document_type_validator = updated_document_type.validators[0]

    assert len(updated_document_type_validator.rules.keys()) == 2
    assert updated_document_type_validator.rules[new_rule_name].name == new_rule_name
    assert updated_document_type_validator.rules[new_rule_name].severity == Severity.ERROR


def test_save__doc_type_exists__validators_added__doc_type_updated(
    document_type_repository,
    document_type,
):
    document_type_repository.save(document_type)

    new_validator_code_1 = "test code 1"
    # fmt: off
    document_type \
        .add_key_value_validator(code=new_validator_code_1) \
        .with_description() \
        .with_key() \
        .with_string_value() \
        .is_required() \
        .build()
    # fmt: on

    new_validator_code_2 = "test code 2"
    # fmt: off
    document_type \
        .add_list_validator(code=new_validator_code_2) \
        .with_description() \
        .for_string_item() \
        .is_required() \
        .build()
    # fmt: on

    new_validator_code_3 = "test code 3"
    # fmt: off
    document_type \
        .add_table_validator(code=new_validator_code_3) \
        .with_description() \
        .for_string_column(index=0, is_required=True) \
        .for_number_column(index=1, is_required=False) \
        .for_boolean_column(index=2, is_required=True) \
        .for_range_column(index=3, is_required=False) \
        .for_date_column(index=4, is_required=False) \
        .with_format(format="format") \
        .for_time_column(index=5, is_required=True) \
        .for_enum_column(index=6, is_required=False) \
        .with_options(options=["op1", "op2"]) \
        .is_required() \
        .build()
    # fmt: on

    document_type_repository.save(document_type)

    updated_document_type = document_type_repository.document_type_of_id(
        document_type.id(),
        document_type.tenant_id(),
    )

    assert len(updated_document_type.validators) == 3
    assert updated_document_type.validators[0].code.value == new_validator_code_1
    assert updated_document_type.validators[1].code.value == new_validator_code_2
    assert updated_document_type.validators[2].code.value == new_validator_code_3


def test_save_all__new_document_types_with_validators(
    document_type_repository,
    document_type_with_string_validator_and_one_rule,
    document_type_id,
    tenant_id,
):
    document_type_with_key_value_validator = DocumentType(
        id_=document_type_id,
        tenant_id=tenant_id,
    )
    # fmt: off
    document_type_with_key_value_validator \
        .add_key_value_validator(code=uuid4().hex) \
        .with_description() \
        .with_key() \
        .with_date_value() \
        .is_required() \
        .build()
    # fmt: on

    document_types_to_save = [
        document_type_with_string_validator_and_one_rule,
        document_type_with_key_value_validator,
    ]
    document_type_repository.save_all(document_types_to_save)

    saved_document_type1 = document_type_repository.document_type_of_id(
        document_type_with_string_validator_and_one_rule.id(),
        document_type_with_string_validator_and_one_rule.tenant_id(),
    )
    saved_document_type2 = document_type_repository.document_type_of_id(
        document_type_with_key_value_validator.id(),
        document_type_with_key_value_validator.tenant_id(),
    )

    assert document_type_with_string_validator_and_one_rule == saved_document_type1
    assert document_type_with_key_value_validator == saved_document_type2


def test_save_new__doc_type_exists__not_updated(
    document_type_repository, document_type, document_type_with_string_validator_and_one_rule
):
    document_type_repository.save(document_type_with_string_validator_and_one_rule)
    document_type_repository.save_new(document_type)

    document_type_result = document_type_repository.document_type_of_id(document_type.id(), document_type.tenant_id())

    assert document_type_result == document_type_with_string_validator_and_one_rule


def test_save_new_all__doc_type_exists__not_updated(
    document_type_repository, document_type, document_type_with_string_validator_and_one_rule
):
    document_type_repository.save(document_type_with_string_validator_and_one_rule)
    document_type_repository.save_new_all([document_type])
    document_type_result = document_type_repository.document_type_of_id(document_type.id(), document_type.tenant_id())

    assert document_type_result == document_type_with_string_validator_and_one_rule


def test_save__document_type_with_cross_field_validator__ok(document_type_repository, document_type_with_validators):
    document_type = document_type_with_validators

    validator_id = document_type.add_cross_field_validator(
        name="test_validator",
        description="Test validator description",
        rule="Ffield1 == Ffield2",
        severity=Severity.ERROR,
        validated_fields=["field1", "field2"],
        issue_message="Fields ${field1} and ${field2} must match",
        dependent_fields=["field1", "field2"],
    )

    document_type_repository.save(document_type)

    saved_document_type = document_type_repository.document_type_of_id(document_type.id(), document_type.tenant_id())

    assert len(saved_document_type.cross_field_validators) == 1
    saved_validator = saved_document_type.cross_field_validators[0]
    assert saved_validator.id() == validator_id
    assert saved_validator.name == "test_validator"
    assert saved_validator.description == "Test validator description"
    assert saved_validator.rule == "Ffield1 == Ffield2"
    assert saved_validator.severity == Severity.ERROR
    assert len(saved_validator.validated_fields) == 2
    assert saved_validator.validated_fields[0].value == "field1"
    assert saved_validator.validated_fields[1].value == "field2"
    assert saved_validator.issue_message.message == "Fields ${field1} and ${field2} must match"
    assert len(saved_validator.issue_message.dependent_fields) == 2
    assert saved_validator.issue_message.dependent_fields[0].value == "field1"
    assert saved_validator.issue_message.dependent_fields[1].value == "field2"

    for validator in saved_document_type.cross_field_validators:
        if validator.id() == validator_id:
            validator.name = "new_name"
            validator.description = "Updated description"
            validator.rule = "Ffield3 == Ffield4"
            validator.validated_fields = [EntityCode("field3")]
            validator.issue_message = CrossFieldIssueMessage(
                message="Fields ${field3} and ${field4} must match",
                dependent_fields=[EntityCode("field4")],
            )

    document_type_repository.save(saved_document_type)

    updated_document_type = document_type_repository.document_type_of_id(document_type.id(), document_type.tenant_id())
    updated_validator = next(v for v in updated_document_type.cross_field_validators if v.id() == validator_id)
    assert updated_validator.name == "new_name"
    assert updated_validator.description == "Updated description"
    assert updated_validator.rule == "Ffield3 == Ffield4"


def test_add_cross_field_validator__integration__success(document_type_repository, document_type_with_validators):
    document_type = document_type_with_validators

    validator_id = document_type.add_cross_field_validator(
        name="integration_validator",
        description="Integration test validator",
        rule="Ffield1 == Ffield2",
        severity=Severity.ERROR,
        validated_fields=["field1", "field2"],
        issue_message="Fields ${field1} and ${field2} must match",
        dependent_fields=["field1", "field2"],
    )

    document_type_repository.save(document_type)

    saved_document_type = document_type_repository.document_type_of_id(document_type.id(), document_type.tenant_id())
    assert len(saved_document_type.cross_field_validators) == 1

    validator = saved_document_type.cross_field_validators[0]
    assert validator.id() == validator_id
    assert validator.name == "integration_validator"
    assert validator.description == "Integration test validator"
    assert validator.rule == "Ffield1 == Ffield2"
    assert validator.severity == Severity.ERROR
    assert len(validator.validated_fields) == 2
    assert validator.validated_fields[0].value == "field1"
    assert validator.validated_fields[1].value == "field2"
    assert validator.issue_message.message == "Fields ${field1} and ${field2} must match"
    assert len(validator.issue_message.dependent_fields) == 2
    assert validator.issue_message.dependent_fields[0].value == "field1"
    assert validator.issue_message.dependent_fields[1].value == "field2"


def test_delete_cross_field_validator__integration__success(document_type_repository, document_type_with_validators):
    document_type = document_type_with_validators

    validator_id = document_type.add_cross_field_validator(
        name="validator_to_delete",
        description="Validator that will be deleted",
        rule="Ffield1 == Ffield2",
        severity=Severity.ERROR,
        validated_fields=["field1", "field2"],
        issue_message="Fields ${field1} and ${field2} must match",
        dependent_fields=["field1", "field2"],
    )

    document_type_repository.save(document_type)

    saved_document_type = document_type_repository.document_type_of_id(document_type.id(), document_type.tenant_id())
    assert len(saved_document_type.cross_field_validators) == 1
    assert saved_document_type.cross_field_validators[0].id() == validator_id

    saved_document_type.remove_cross_field_validator(validator_id=validator_id)

    document_type_repository.save(saved_document_type)

    updated_document_type = document_type_repository.document_type_of_id(document_type.id(), document_type.tenant_id())
    assert len(updated_document_type.cross_field_validators) == 0


def test_delete_cross_field_validator__integration__nonexistent_validator(
    document_type_repository, document_type_with_validators
):
    document_type = document_type_with_validators

    validator_id = document_type.add_cross_field_validator(
        name="existing_validator",
        description="This validator should remain after deletion attempt",
        rule="Ffield1 == Ffield2",
        severity=Severity.ERROR,
        validated_fields=["field1", "field2"],
        issue_message="Fields ${field1} and ${field2} must match",
        dependent_fields=["field1", "field2"],
    )

    document_type_repository.save(document_type)

    saved_document_type = document_type_repository.document_type_of_id(document_type.id(), document_type.tenant_id())

    non_existent_id = "non-existent-validator-id"
    saved_document_type.remove_cross_field_validator(validator_id=non_existent_id)
    document_type_repository.save(saved_document_type)

    updated_document_type = document_type_repository.document_type_of_id(document_type.id(), document_type.tenant_id())
    assert len(updated_document_type.cross_field_validators) == 1
    assert updated_document_type.cross_field_validators[0].id() == validator_id
