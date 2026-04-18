import pytest

from deps_high_sparrow.domain.model import (
    DocumentArtifact,
    DocumentTypeFactory,
    Severity,
    ValidationResult,
)


@pytest.fixture
def document_type_cross_rules(
    document_type_id,
    tenant_id,
    entity_code_1,
    entity_code_2,
    entity_code_3,
):
    document_type = DocumentTypeFactory.create(
        id_=document_type_id,
        tenant_id=tenant_id,
    )
    document_type.add_string_validator(entity_code_1).with_description().is_required().build()
    document_type.add_string_validator(entity_code_2).with_description().is_required().build()
    document_type.add_string_validator(entity_code_3).with_description().build()

    document_type.add_cross_field_validator(
        name="field1_equals_field2",
        description="Field1 must equal Field2",
        rule=f"F{entity_code_1} == F{entity_code_2}",
        severity=Severity.ERROR,
        validated_fields=[entity_code_1],
        issue_message=f"Field1 must match ${{{entity_code_2}}}",
        dependent_fields=[entity_code_2],
    )

    document_type.add_cross_field_validator(
        name="field2_not_empty",
        description="Field2 must not be empty",
        rule=f"F{entity_code_2} != ''",
        severity=Severity.WARNING,
        validated_fields=[entity_code_2],
        issue_message="Field2 must not be empty",
        dependent_fields=[],
    )

    return document_type


@pytest.fixture
def artifacts_two_fields(entity_code_1, entity_code_2):
    return [
        DocumentArtifact(entity_code_1, "value1"),
        DocumentArtifact(entity_code_2, "value2"),
    ]


@pytest.fixture
def artifacts_field1_absent(entity_code_1, entity_code_2):
    return [
        DocumentArtifact(entity_code_1, None),
        DocumentArtifact(entity_code_2, "value2"),
    ]


@pytest.fixture
def artifacts_field1_present(entity_code_1, entity_code_2):
    return [
        DocumentArtifact(entity_code_1, "valid_value"),
        DocumentArtifact(entity_code_2, "value2"),
    ]


@pytest.fixture
def artifacts_field3_only(entity_code_3):
    return [
        DocumentArtifact(entity_code_3, None),
    ]


@pytest.fixture
def artifacts_field1_only(entity_code_1):
    return [
        DocumentArtifact(entity_code_1, "value1"),
    ]


@pytest.fixture
def unknown_field_code():
    return "non_existent_field"


@pytest.fixture
def validation_result_blank(document_id, tenant_id):
    return ValidationResult(document_id, tenant_id)


@pytest.fixture
def document_type_field1_invalid(
    document_type_cross_rules,
    document_id,
    entity_code_1,
    validation_result_blank,
    artifacts_field1_absent,
):
    document_type = document_type_cross_rules
    document_type.record_field_validation(
        document_id=document_id,
        field_code=entity_code_1,
        document_artifacts=artifacts_field1_absent,
        validation_result=validation_result_blank,
    )
    return document_type


@pytest.fixture
def validation_result_field1_one_issue(
    document_type_field1_invalid,
    entity_code_1,
):
    result = document_type_field1_invalid.derive_validation_result()
    assert len(result.issues[entity_code_1]()) == 1
    return result


@pytest.fixture
def document_type_field3_invalid(
    document_type_cross_rules,
    document_id,
    entity_code_3,
    validation_result_blank,
    artifacts_field3_only,
):
    document_type = document_type_cross_rules
    document_type.record_field_validation(
        document_id=document_id,
        field_code=entity_code_3,
        document_artifacts=artifacts_field3_only,
        validation_result=validation_result_blank,
    )
    return document_type


@pytest.fixture
def validation_result_field3_issues(
    document_type_field3_invalid,
    entity_code_3,
):
    result = document_type_field3_invalid.derive_validation_result()
    assert entity_code_3 in result.issues
    return result


@pytest.fixture
def document_type_string_only(document_type_id, tenant_id, entity_code_1):
    document_type = DocumentTypeFactory.create(
        id_=document_type_id,
        tenant_id=tenant_id,
    )
    document_type.add_string_validator(entity_code_1).with_description().is_required().build()
    return document_type
