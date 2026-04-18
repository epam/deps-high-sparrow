from collections import defaultdict
from typing import DefaultDict, Optional

from deps_high_sparrow.constants import ENCODED_SLASH

from ....exceptions import RuleAlreadyExistsError
from ...shared import EntityCode, Guard, ImmutableCheck, Severity
from ...validation_result import Issues
from ..document_artifact import Value
from ..operand_type import OperandType
from .preparer import (
    AbstractPreparer,
    KeyValuePreparer,
    ListPreparer,
    SeparatedValuePreparer,
    TablePreparer,
)
from .rule import Rule
from .validation.entities import RuleEntity, RuleEntityMeta
from .validation.services import (
    BusinessRulesValidationService,
    FieldCasterService,
    RequiredFieldsPreCheckService,
    TypeValidationService,
)
from .validator_type import ValidatorType

__all__ = ["Validator"]


class Validator:
    code = Guard[EntityCode](EntityCode, ImmutableCheck())
    type_ = Guard[ValidatorType](ValidatorType, ImmutableCheck())
    is_required = Guard[bool](bool, ImmutableCheck())
    rules = Guard[dict[str, list[Rule]]](dict)

    def __init__(
        self,
        code: str,
        type_: ValidatorType,
        is_required: bool,
        *,
        rules: Optional[dict[str, Rule]] = None,
    ):
        self.code = EntityCode(code)
        self.type_ = type_
        self.is_required = is_required

        self.rules = rules or {}

        self._preparers: DefaultDict[OperandType, type[AbstractPreparer]] = defaultdict(lambda: SeparatedValuePreparer)
        self._preparers.update(
            {
                OperandType.TABLE: TablePreparer,
                OperandType.DICT: KeyValuePreparer,
                OperandType.ARRAY: ListPreparer,
            }
        )

        self._required_value_checker = RequiredFieldsPreCheckService()
        self._type_checker = TypeValidationService()
        self._value_caster = FieldCasterService()
        self._business_rules_checker = BusinessRulesValidationService()

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.code == other.code

    @property
    def preparer(self) -> type[AbstractPreparer]:
        return self._preparers[self.type_.type]

    def add_rule(
        self,
        name: str,
        severity: Severity,
        rule: str,
        issue_message: str,
        *,
        description: str = "",
        need_warning_even_if_optional: bool = False,
        for_each: bool = False,
        for_any: bool = False,
        check_optional_fields: bool = False,
    ) -> Rule:
        self._check_rule_uniqueness(name=name)
        rule_to_add = Rule(
            name=name,
            severity=severity,
            rule=rule,
            issue_message=issue_message,
            description=description,
            need_warning_even_if_optional=need_warning_even_if_optional,
            for_each=for_each,
            for_any=for_any,
            check_optional_fields=check_optional_fields,
        )
        self.rules[name] = rule_to_add
        return rule_to_add

    def delete_rule(self, name: str) -> None:
        new_name = self._convert_encoded_slash(name)
        if new_name in self.rules:
            del self.rules[new_name]

    def validate(self, value: Optional[Value]) -> Issues:
        issues = Issues(self.code)

        if value is None:
            return self._validate_empty_value(issues)

        data_to_validate = self.preparer(
            self.code,
            self.type_,
            self.is_required,
        ).prepare(value)

        self._required_value_checker.perform_validation(data_to_validate, issues)
        self._type_checker.perform_validation(data_to_validate, issues)

        if issues.is_valid:
            self._business_rules_checker.perform_validation(
                field=self._value_caster.cast_field(data_to_validate),
                rules=self._prepare_rules(),
                issues=issues,
            )
        return issues

    def _validate_empty_value(self, issues: Issues) -> Issues:
        if self.is_required:
            self._required_value_checker.create_issues_for_empty_value(self.code(), issues)
        return issues

    def _prepare_rules(self) -> list[RuleEntity]:
        return [
            RuleEntity(
                0,
                rule.name,
                rule.severity.value,
                self.code(),
                "type_code",
                rule.rule,
                rule.issue_message,
                meta=RuleEntityMeta(
                    rule.need_warning_even_if_optional,
                    rule.for_each,
                    rule.for_any,
                    rule.check_optional_fields,
                ),
            )
            for rule in self.rules.values()
        ]

    def _check_rule_uniqueness(self, name: str) -> None:
        if name in self.rules:
            raise RuleAlreadyExistsError(name)

    def _convert_encoded_slash(self, name: str) -> str:
        return name.replace(ENCODED_SLASH, "/")
