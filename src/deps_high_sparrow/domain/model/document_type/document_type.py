import uuid
from typing import List, Optional, Set

from deps_high_sparrow.constants import (
    MAX_EXTERNAL_VALIDATORS,
    MAX_LENGTH_DESCRIPTION_FIELD_VALIDATORS,
)
from deps_high_sparrow.domain.model.validation_result import CrossFieldIssueMessage

from ...exceptions import (
    CrossFieldValidatorAlreadyExistsError,
    CrossFieldValidatorNotFound,
    ExternalValidatorAlreadyExistsError,
    InvalidFieldCodesError,
    MaxCrossFieldValidatorsExceededError,
    MaxExternalValidatorsExceededError,
    ValidatorNotFound,
    WrongCrossFieldValidatorMessageError,
)
from ..shared import EntityCode, EntityId, Guard, ImmutableCheck, Severity, TenantId
from ..validation_result import RawIssues, ValidationResult
from .cross_field_validator import CrossFieldValidator
from .document_artifact import DocumentArtifact, Value
from .external_validator import ExternalValidator
from .external_validator_name import ExternalValidatorName
from .operand_type import OperandType
from .validator import Rule, Validator, ValidatorBuilder

__all__ = ["DocumentType"]


class DocumentType:
    id = Guard[EntityId](EntityId, ImmutableCheck())
    tenant_id = Guard[TenantId](TenantId, ImmutableCheck())

    def __init__(
        self,
        id_: str,
        tenant_id: str,
        *,
        validators: Optional[list[Validator]] = None,
        external_validators: Optional[list[ExternalValidator]] = None,
        cross_field_validators: Optional[list[CrossFieldValidator]] = None,
    ) -> None:
        self.id = EntityId(id_)
        self.tenant_id = TenantId(tenant_id)

        self._validators: dict[str, Validator] = {validator.code(): validator for validator in validators or []}
        self._external_validators: dict[str, ExternalValidator] = {
            external_validator.name: external_validator for external_validator in external_validators or []
        }
        self._cross_field_validators: dict[str, CrossFieldValidator] = {
            cross_field_validator.id(): cross_field_validator for cross_field_validator in cross_field_validators or []
        }
        self._validation_data = None

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.id == other.id

    def __repr__(self) -> str:
        return "\n".join(
            (
                f"<class '{self.__class__.__name__}':",
                f"{self.id = },",
                f"{self.tenant_id = },",
                f"{self._validators = }>",
                f"{self._external_validators = }>",
            ),
        )

    @property
    def validators(self) -> list[Validator]:
        return list(self._validators.values())

    @property
    def external_validators(self) -> list[ExternalValidator]:
        return list(self._external_validators.values())

    @property
    def has_external_validators(self) -> bool:
        return bool(self.external_validators)

    @property
    def cross_field_validators(self) -> list[CrossFieldValidator]:
        return list(self._cross_field_validators.values())

    @property
    def has_cross_field_validators(self) -> bool:
        return bool(self.cross_field_validators)

    def add_string_validator(self, code: str) -> ValidatorBuilder:
        return self._ValidatorBuilder(code=code, type=OperandType.STRING, parent=self)

    def add_number_validator(self, code: str) -> ValidatorBuilder:
        return self._ValidatorBuilder(code=code, type=OperandType.NUMBER, parent=self)

    def add_boolean_validator(self, code: str) -> ValidatorBuilder:
        return self._ValidatorBuilder(code=code, type=OperandType.BOOL, parent=self)

    def add_range_validator(self, code: str) -> ValidatorBuilder:
        return self._ValidatorBuilder(code=code, type=OperandType.RANGE, parent=self)

    def add_date_validator(self, code: str) -> ValidatorBuilder:
        return self._ValidatorBuilder(code=code, type=OperandType.DATE, parent=self)

    def add_time_validator(self, code: str) -> ValidatorBuilder:
        return self._ValidatorBuilder(code=code, type=OperandType.TIME, parent=self)

    def add_datetime_validator(self, code: str) -> ValidatorBuilder:
        return self._ValidatorBuilder(code=code, type=OperandType.DATETIME, parent=self)

    def add_enum_validator(self, code: str) -> ValidatorBuilder:
        return self._ValidatorBuilder(code=code, type=OperandType.ENUM, parent=self)

    def add_key_value_validator(self, code: str) -> ValidatorBuilder:
        return self._ValidatorBuilder(code=code, type=OperandType.DICT, parent=self)

    def add_table_validator(self, code: str) -> ValidatorBuilder:
        return self._ValidatorBuilder(code=code, type=OperandType.TABLE, parent=self)

    def add_list_validator(self, code: str) -> ValidatorBuilder:
        return self._ValidatorBuilder(code=code, type=OperandType.ARRAY, parent=self)

    def remove_validator(self, code: str) -> None:
        if code in self._validators:
            del self._validators[code]

    def add_error_check_to_validator(
        self,
        code: str,
        name: str,
        rule: str,
        issue_message: str,
        *,
        need_warning_even_if_optional: bool = False,
        for_each: bool = False,
        for_any: bool = False,
        check_optional_fields: bool = False,
    ) -> None:
        self._add_rule_to_validator(
            code=code,
            name=name,
            severity=Severity.ERROR,
            rule=rule,
            issue_message=issue_message,
            need_warning_even_if_optional=need_warning_even_if_optional,
            for_each=for_each,
            for_any=for_any,
            check_optional_fields=check_optional_fields,
        )

    def add_warning_check_to_validator(
        self,
        code: str,
        name: str,
        rule: str,
        issue_message: str,
        *,
        need_warning_even_if_optional: bool = False,
        for_each: bool = False,
        for_any: bool = False,
        check_optional_fields: bool = False,
    ) -> None:
        self._add_rule_to_validator(
            code=code,
            name=name,
            severity=Severity.WARNING,
            rule=rule,
            issue_message=issue_message,
            need_warning_even_if_optional=need_warning_even_if_optional,
            for_each=for_each,
            for_any=for_any,
            check_optional_fields=check_optional_fields,
        )

    def record_external_validation(self, validators_issues: dict[ExternalValidatorName, list[RawIssues]]) -> None:
        for validator_name, raw_issues_list in validators_issues.items():
            external_validator = self._external_validators[validator_name]
            issues_list = external_validator.validate(raw_issues_list)

            for issues in issues_list:
                self._validation_data.add_issues(issues)

    def record_local_validation(self, document_id: str, document_artifacts: list[DocumentArtifact]) -> None:
        self._validation_data = ValidationResult(document_id, self.tenant_id())

        prepared_artifacts = self._prepare_document_artifacts(document_artifacts)

        for validator in self._validators.values():
            self._validation_data.add_issues(
                validator.validate(prepared_artifacts.get(validator.code, None)),
            )

        for cross_field_validator in self._cross_field_validators.values():
            cross_field_issues_list = cross_field_validator.validate(
                prepared_artifacts,
                validators={
                    EntityCode(validator_code): validator_item
                    for validator_code, validator_item in self._validators.items()
                },
            )

            for cross_field_issues in cross_field_issues_list:
                self._validation_data.add_cross_field_issues(cross_field_issues)

    def record_field_validation(
        self,
        document_id: str,
        field_code: str,
        document_artifacts: list[DocumentArtifact],
        validation_result: ValidationResult | None = None,
    ) -> None:
        self._validation_data = validation_result or ValidationResult(document_id, self.tenant_id())

        prepared_artifacts = self._prepare_document_artifacts(document_artifacts)
        field_code_entity = EntityCode(field_code)

        if field_code in self._validators:
            validator = self._validators[field_code]
            issues = validator.validate(prepared_artifacts.get(validator.code, None))
            self._validation_data.replace_issues(issues)

        relevant_cross_field_validators = [
            cfv for cfv in self._cross_field_validators.values() if field_code_entity in cfv.validated_fields
        ]

        for cross_field_validator in relevant_cross_field_validators:
            cross_field_issues_list = cross_field_validator.validate(
                prepared_artifacts,
                validators={
                    EntityCode(validator_code): validator_item
                    for validator_code, validator_item in self._validators.items()
                },
            )

            for cross_field_issues in cross_field_issues_list:
                self._validation_data.replace_cross_field_issues(cross_field_issues)

    def derive_validation_result(self) -> ValidationResult:
        return self._validation_data

    def get_validator(self, code: str) -> Validator:
        if (validator := self._validators.get(code)) is None:
            raise ValidatorNotFound(code)

        return validator

    def attach_external_validator(self, name: str, url: str) -> None:
        self._check_max_external_validators_not_exceeded()
        self._check_external_validators_name_uniqueness(name)

        self._external_validators[name] = ExternalValidator(name=name, url=url)

    def remove_external_validator(self, name: str) -> None:
        if name in self._external_validators:
            del self._external_validators[name]

    def add_rules_to_validator(self, code: str, rules: list[Rule]) -> None:
        validator = self.get_validator(code)

        for rule in rules:
            validator.add_rule(
                name=rule.name,
                severity=rule.severity,
                rule=rule.rule,
                issue_message=rule.issue_message,
                description=rule.description,
                need_warning_even_if_optional=rule.need_warning_even_if_optional,
                for_each=rule.for_each,
                for_any=rule.for_any,
                check_optional_fields=rule.check_optional_fields,
            )

    def add_cross_field_validator(
        self,
        name: str,
        description: str,
        rule: str,
        severity: Severity,
        validated_fields: List[str],
        issue_message: str,
        dependent_fields: List[str],
        for_each: bool = False,
        for_any: bool = False,
    ) -> str:
        all_fields = set(validated_fields + dependent_fields)

        self._check_cross_field_validator_message(issue_message, dependent_fields)
        self._check_max_cross_field_validators_not_exceeded()
        self._check_cross_field_validators_name_uniqueness(name)
        self._validate_field_codes(all_fields)

        validator_id = uuid.uuid4().hex

        cross_field_validator = CrossFieldValidator.make(
            id_=validator_id,
            name=name,
            description=description,
            rule=rule,
            severity=severity,
            validated_fields=validated_fields,
            issue_message=issue_message,
            dependent_fields=dependent_fields,
            for_each=for_each,
            for_any=for_any,
        )

        self._cross_field_validators[validator_id] = cross_field_validator
        return validator_id

    def update_cross_field_validator(
        self,
        validator_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        rule: Optional[str] = None,
        severity: Optional[Severity] = None,
        validated_fields: Optional[list[str]] = None,
        issue_message: Optional[str] = None,
        dependent_fields: Optional[list[str]] = None,
        for_each: Optional[bool] = None,
        for_any: Optional[bool] = None,
    ) -> None:
        if validator_id not in self._cross_field_validators:
            raise CrossFieldValidatorNotFound(validator_id)

        cross_field_validator = self._cross_field_validators[validator_id]

        if name is not None and name != cross_field_validator.name:
            self._check_cross_field_validators_name_uniqueness(name)

        all_fields = set((validated_fields or []) + (dependent_fields or []))
        self._validate_field_codes(all_fields)

        name = name if name is not None else cross_field_validator.name
        description = description if description is not None else cross_field_validator.description
        rule = rule if rule is not None else cross_field_validator.rule
        severity = severity if severity is not None else cross_field_validator.severity
        for_each_value = for_each if for_each is not None else cross_field_validator.for_each
        for_any_value = for_any if for_any is not None else cross_field_validator.for_any
        validated_fields_codes: list[EntityCode] = (
            [EntityCode(field) for field in validated_fields]
            if validated_fields is not None
            else cross_field_validator.validated_fields
        )
        dependent_fields_codes: list[EntityCode] = (
            [EntityCode(field) for field in dependent_fields]
            if dependent_fields is not None
            else cross_field_validator.issue_message.dependent_fields
        )
        issue_message = issue_message if issue_message is not None else cross_field_validator.issue_message.message

        cross_field_issue_message = CrossFieldIssueMessage(
            message=issue_message, dependent_fields=dependent_fields_codes
        )

        cross_field_validator.update(
            name=name,
            description=description,
            rule=rule,
            severity=severity,
            validated_fields=validated_fields_codes,
            issue_message=cross_field_issue_message,
            for_each=for_each_value,
            for_any=for_any_value,
        )

    def remove_cross_field_validator(self, validator_id) -> None:
        if validator_id in self._cross_field_validators:
            del self._cross_field_validators[validator_id]

    def fields_to_validate_with(self, field_code: str) -> list[str]:
        field_codes = {field_code}

        for cross_field_validator in self._cross_field_validators.values():
            validated_field_codes = {field.value for field in cross_field_validator.validated_fields}
            if field_code in validated_field_codes:
                field_codes.update(validated_field_codes)
                dependent_field_codes = {field.value for field in cross_field_validator.issue_message.dependent_fields}
                field_codes.update(dependent_field_codes)

        return list(field_codes)

    def _get_all_field_codes(self) -> Set[str]:
        return set(self._validators.keys())

    def _get_invalid_field_codes(self, field_codes: Set[str]) -> List[str]:
        valid_fields = self._get_all_field_codes()
        return list(field_codes - valid_fields)

    def _validate_field_codes(self, all_fields):
        invalid_fields = self._get_invalid_field_codes(all_fields)
        if invalid_fields:
            raise InvalidFieldCodesError(invalid_fields)

    def _add_rule_to_validator(
        self,
        code: str,
        name: str,
        severity: Severity,
        rule: str,
        issue_message: str,
        *,
        need_warning_even_if_optional: bool = False,
        for_each: bool = False,
        for_any: bool = False,
        check_optional_fields: bool = False,
    ) -> None:
        validator = self.get_validator(code)
        validator.add_rule(
            name=name,
            severity=severity,
            rule=rule,
            issue_message=issue_message,
            need_warning_even_if_optional=need_warning_even_if_optional,
            for_each=for_each,
            for_any=for_any,
            check_optional_fields=check_optional_fields,
        )

    def _check_max_external_validators_not_exceeded(self) -> None:
        if len(self._external_validators) >= MAX_EXTERNAL_VALIDATORS:
            raise MaxExternalValidatorsExceededError(
                f"The number of external validators per document type can't exceed {MAX_EXTERNAL_VALIDATORS}"
            )

    def _check_external_validators_name_uniqueness(self, name: str) -> None:
        if name in self._external_validators:
            raise ExternalValidatorAlreadyExistsError(
                f"External validator with name `{name}` already exits for document type with id `{self.id.value}`"
            )

    def _check_cross_field_validators_name_uniqueness(self, name: str) -> None:
        for validator in self._cross_field_validators.values():
            if validator.name == name:
                raise CrossFieldValidatorAlreadyExistsError(
                    f"Cross field validator with name `{name}` already exists for document type id `{self.id.value}`"
                )

    def _check_max_cross_field_validators_not_exceeded(self) -> None:
        if len(self._cross_field_validators) >= MAX_LENGTH_DESCRIPTION_FIELD_VALIDATORS:
            raise MaxCrossFieldValidatorsExceededError(
                f"The number of cross-field validators per document type can't exceed "
                f"{MAX_LENGTH_DESCRIPTION_FIELD_VALIDATORS}"
            )

    @staticmethod
    def _check_cross_field_validator_message(issue_message: str, dependent_fields: list[str]) -> None:
        for dependent_field in dependent_fields:
            if f"${{{dependent_field}}}" not in issue_message:
                raise WrongCrossFieldValidatorMessageError(
                    "Cross field message placeholders are not mapped with dependent fields"
                )

    def _prepare_document_artifacts(self, document_artifacts: list[DocumentArtifact]) -> dict[EntityCode, Value]:
        edata_mapping = {document_artifact.code: document_artifact.value for document_artifact in document_artifacts}
        empty_fields_mapping = {
            EntityCode(code): None for code in self._validators.keys() if EntityCode(code) not in edata_mapping
        }

        return edata_mapping | empty_fields_mapping

    class _ValidatorBuilder(ValidatorBuilder):
        def _add_to_parent(self) -> None:
            self._parent._validators[self._code] = self._build()
