import pytest

from deps_high_sparrow.application import RuleService
from deps_high_sparrow.constants import ENCODED_SLASH
from deps_high_sparrow.domain.exceptions import (
    DocumentTypeNotFound,
    RuleAlreadyExistsError,
    ValidatorNotFound,
)
from deps_high_sparrow.domain.model import IDocumentTypeRepository, Rule


class TestRuleService:
    def test_create_rule_doc_type_and_validator_exist__created(
        self,
        fake_document_type_repository: IDocumentTypeRepository,
        rule_service: RuleService,
        document_type_with_string_validator,
        validator_code,
        rule_name,
        rule_severity,
        rule_text,
        rule_issue_message,
        rule_description,
        rule_need_warning_even_if_optional,
        rule_for_each,
        rule_for_any,
        rule_check_optional_fields,
    ):
        fake_document_type_repository.save(document_type_with_string_validator)
        created_rule = rule_service.create_rule(
            document_type_id=document_type_with_string_validator.id(),
            tenant_id=document_type_with_string_validator.tenant_id(),
            validator_code=validator_code,
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

        assert isinstance(created_rule, Rule)
        assert created_rule.name == rule_name
        assert created_rule.severity == rule_severity
        assert created_rule.rule == rule_text
        assert created_rule.issue_message == rule_issue_message
        assert created_rule.need_warning_even_if_optional == rule_need_warning_even_if_optional
        assert created_rule.for_each == rule_for_each
        assert created_rule.for_any == rule_for_any
        assert created_rule.check_optional_fields == rule_check_optional_fields

    def test_create_rule_doc_type_not_exists__raises(
        self,
        fake_document_type_repository: IDocumentTypeRepository,
        rule_service: RuleService,
        document_type,
        validator_code,
        rule_name,
        rule_severity,
        rule_text,
        rule_issue_message,
        rule_description,
        rule_need_warning_even_if_optional,
        rule_for_each,
        rule_for_any,
        rule_check_optional_fields,
    ):
        with pytest.raises(DocumentTypeNotFound):
            rule_service.create_rule(
                document_type_id=document_type.id(),
                tenant_id=document_type.tenant_id(),
                validator_code=validator_code,
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

    def test_create_rule_doc_type_exists_validator_not_exist_raises(
        self,
        fake_document_type_repository: IDocumentTypeRepository,
        rule_service: RuleService,
        document_type,
        validator_code,
        rule_name,
        rule_severity,
        rule_text,
        rule_issue_message,
        rule_description,
        rule_need_warning_even_if_optional,
        rule_for_each,
        rule_for_any,
        rule_check_optional_fields,
    ):
        fake_document_type_repository.save(document_type)
        with pytest.raises(ValidatorNotFound):
            rule_service.create_rule(
                document_type_id=document_type.id(),
                tenant_id=document_type.tenant_id(),
                validator_code=validator_code,
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

    def test_create_rule_doc_type_and_validator_exist_rule_already_exists__raises(
        self,
        fake_document_type_repository: IDocumentTypeRepository,
        rule_service: RuleService,
        document_type_with_string_validator_and_one_rule,
        validator_code,
        rule_name,
        rule_severity,
        rule_text,
        rule_issue_message,
        rule_description,
        rule_need_warning_even_if_optional,
        rule_for_each,
        rule_for_any,
        rule_check_optional_fields,
    ):
        fake_document_type_repository.save(document_type_with_string_validator_and_one_rule)
        with pytest.raises(RuleAlreadyExistsError):
            rule_service.create_rule(
                document_type_id=document_type_with_string_validator_and_one_rule.id(),
                tenant_id=document_type_with_string_validator_and_one_rule.tenant_id(),
                validator_code=validator_code,
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

    def test_delete_rule_doc_type_and_validator_exist__deleted(
        self,
        fake_document_type_repository: IDocumentTypeRepository,
        rule_service: RuleService,
        document_type_with_string_validator_and_one_rule,
        validator_code,
        rule_name,
        rule_severity,
        rule_text,
        rule_issue_message,
        rule_need_warning_even_if_optional,
        rule_for_each,
        rule_for_any,
        rule_check_optional_fields,
        document_type_id,
        tenant_id,
    ):
        fake_document_type_repository.save(document_type_with_string_validator_and_one_rule)

        rule_service.delete_rule(
            document_type_id=document_type_id,
            tenant_id=tenant_id,
            validator_code=validator_code,
            name=rule_name,
        )

        updated_document_type = fake_document_type_repository.document_type_of_id(
            document_type_id=document_type_id,
            tenant_id=tenant_id,
        )
        validator = updated_document_type.get_validator(validator_code)

        assert rule_name not in validator.rules

    def test_delete_rule_doc_type_and_validator_with_slash__deleted(
        self,
        fake_document_type_repository: IDocumentTypeRepository,
        rule_service: RuleService,
        document_type_with_string_validator_and_one_rule_with_slash,
        validator_code,
        rule_name_with_slash,
        rule_severity,
        document_type_id,
        tenant_id,
    ):
        fake_document_type_repository.save(document_type_with_string_validator_and_one_rule_with_slash)

        encoded_rule_name = rule_name_with_slash.replace("/", ENCODED_SLASH)

        rule_service.delete_rule(
            document_type_id=document_type_id,
            tenant_id=tenant_id,
            validator_code=validator_code,
            name=encoded_rule_name,
        )

        updated_document_type = fake_document_type_repository.document_type_of_id(
            document_type_id=document_type_id,
            tenant_id=tenant_id,
        )
        validator = updated_document_type.get_validator(validator_code)

        assert rule_name_with_slash not in validator.rules

    @pytest.mark.document_type
    def test_add_cross_field_validator__valid_parameters__succeeds(
        self,
        fake_document_type_repository,
        document_type_service,
        document_type_with_validators,
        document_type_id,
        tenant_id,
        cross_field_validator_name,
        cross_field_validator_description,
        cross_field_validator_rule,
        cross_field_validator_severity,
        cross_field_validated_fields,
        cross_field_issue_message_text,
        cross_field_dependent_fields,
    ):
        fake_document_type_repository.save(document_type_with_validators)

        validated_fields_str = [field.value for field in cross_field_validated_fields]
        dependent_fields_str = [field.value for field in cross_field_dependent_fields]

        validator_id = document_type_service.add_cross_field_validator(
            tenant_id=tenant_id,
            document_type_id=document_type_id,
            name=cross_field_validator_name,
            description=cross_field_validator_description,
            rule=cross_field_validator_rule,
            severity=cross_field_validator_severity,
            validated_fields=validated_fields_str,
            issue_message=cross_field_issue_message_text,
            dependent_fields=dependent_fields_str,
        )

        saved_document_type = fake_document_type_repository.document_type_of_id(
            document_type_id=document_type_id,
            tenant_id=tenant_id,
        )
        assert len(saved_document_type.cross_field_validators) == 1

        validator = saved_document_type.cross_field_validators[0]
        assert validator.id() == validator_id
        assert validator.name == cross_field_validator_name
        assert validator.description == cross_field_validator_description
        assert validator.rule == cross_field_validator_rule
        assert validator.severity == cross_field_validator_severity
        assert [field.value for field in validator.validated_fields] == validated_fields_str
        assert validator.issue_message.message == cross_field_issue_message_text
        assert [field.value for field in validator.issue_message.dependent_fields] == dependent_fields_str

    @pytest.mark.document_type
    def test_add_cross_field_validator__with_for_each_for_any__succeeds(
        self,
        fake_document_type_repository,
        document_type_service,
        document_type_with_validators,
        document_type_id,
        tenant_id,
        cross_field_validator_name,
        cross_field_validator_description,
        cross_field_validator_rule,
        cross_field_validator_severity,
        cross_field_validated_fields,
        cross_field_issue_message_text,
        cross_field_dependent_fields,
    ):
        fake_document_type_repository.save(document_type_with_validators)

        validated_fields_str = [field.value for field in cross_field_validated_fields]
        dependent_fields_str = [field.value for field in cross_field_dependent_fields]

        validator_id = document_type_service.add_cross_field_validator(
            tenant_id=tenant_id,
            document_type_id=document_type_id,
            name=cross_field_validator_name,
            description=cross_field_validator_description,
            rule=cross_field_validator_rule,
            severity=cross_field_validator_severity,
            validated_fields=validated_fields_str,
            issue_message=cross_field_issue_message_text,
            dependent_fields=dependent_fields_str,
            for_each=True,
            for_any=True,
        )

        saved_document_type = fake_document_type_repository.document_type_of_id(
            document_type_id=document_type_id,
            tenant_id=tenant_id,
        )
        validator = saved_document_type.cross_field_validators[0]
        assert validator.id() == validator_id
        assert validator.for_each is True
        assert validator.for_any is True

    @pytest.mark.document_type
    def test_add_cross_field_validator__document_type_not_found__raises_error(
        self,
        document_type_service,
        document_type_id,
        tenant_id,
        cross_field_validator_name,
        cross_field_validator_description,
        cross_field_validator_rule,
        cross_field_validator_severity,
        cross_field_validated_fields,
        cross_field_issue_message_text,
        cross_field_dependent_fields,
    ):
        with pytest.raises(DocumentTypeNotFound):
            document_type_service.add_cross_field_validator(
                tenant_id=tenant_id,
                document_type_id=document_type_id,
                name=cross_field_validator_name,
                description=cross_field_validator_description,
                rule=cross_field_validator_rule,
                severity=cross_field_validator_severity,
                validated_fields=[field.value for field in cross_field_validated_fields],
                issue_message=cross_field_issue_message_text,
                dependent_fields=[field.value for field in cross_field_dependent_fields],
            )
