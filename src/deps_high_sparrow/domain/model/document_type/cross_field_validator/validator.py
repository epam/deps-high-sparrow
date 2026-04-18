import logging
from collections import defaultdict
from typing import DefaultDict, List, Mapping, Optional

from deps_high_sparrow.constants import (
    MAX_LENGTH_DESCRIPTION_FIELD_VALIDATORS,
    MAX_LENGTH_NAME_FIELD_VALIDATORS,
    MIN_LENGTH_FIELD_VALIDATORS,
)
from deps_high_sparrow.domain.exceptions import UnparseableRuleError
from deps_high_sparrow.domain.model.document_type.document_artifact import Value
from deps_high_sparrow.domain.model.document_type.operand_type import OperandType
from deps_high_sparrow.domain.model.document_type.validator import Validator
from deps_high_sparrow.domain.model.document_type.validator.preparer import (
    AbstractPreparer,
    KeyValuePreparer,
    ListPreparer,
    SeparatedValuePreparer,
    TablePreparer,
)
from deps_high_sparrow.domain.model.document_type.validator.validation.entities import (
    RuleEntity,
    RuleEntityMeta,
)
from deps_high_sparrow.domain.model.document_type.validator.validation.services import (
    BusinessRulesValidationService,
    FieldCasterService,
)
from deps_high_sparrow.domain.model.document_type.validator.validation.services.utils import (
    FieldValidationIssues,
    Message,
)
from deps_high_sparrow.domain.model.shared import (
    EntityCode,
    EntityId,
    FormatCheck,
    Guard,
    ImmutableCheck,
    LengthCheck,
    Severity,
)
from deps_high_sparrow.domain.model.validation_result import (
    CrossFieldIssue,
    CrossFieldIssueMessage,
    CrossFieldIssues,
    Position,
)

from .rule_validator import RuleFieldReferencesValidator

__all__ = ["CrossFieldValidator"]


class CrossFieldValidator:
    id = Guard[EntityId](EntityId, ImmutableCheck())
    name = Guard[str](
        str,
        LengthCheck(min_length=MIN_LENGTH_FIELD_VALIDATORS, max_length=MAX_LENGTH_NAME_FIELD_VALIDATORS),
        FormatCheck("^[a-zA-Z0-9_-]+$"),
    )
    description = Guard[str](str, LengthCheck(max_length=MAX_LENGTH_DESCRIPTION_FIELD_VALIDATORS))
    rule = Guard[str](str, LengthCheck(min_length=MIN_LENGTH_FIELD_VALIDATORS))
    severity = Guard[Severity](Severity)

    _rule_validator = RuleFieldReferencesValidator()

    def __init__(
        self,
        id_: str,
        name: str,
        description: str,
        rule: str,
        severity: Severity,
        validated_fields: List[EntityCode],
        issue_message: CrossFieldIssueMessage,
        for_each: bool = False,
        for_any: bool = False,
    ) -> None:
        self.id = EntityId(id_)
        self.name = name
        self.description = description
        self.rule = rule
        self.severity = severity
        self.validated_fields = validated_fields
        self.issue_message = issue_message
        self.for_each = for_each
        self.for_any = for_any

        self._value_caster = FieldCasterService()
        self._business_rules_checker = BusinessRulesValidationService()

        self._preparers: DefaultDict[OperandType, type[AbstractPreparer]] = defaultdict(lambda: SeparatedValuePreparer)
        self._preparers.update(
            {
                OperandType.TABLE: TablePreparer,
                OperandType.DICT: KeyValuePreparer,
                OperandType.ARRAY: ListPreparer,
            }
        )

        self._logger = logging.getLogger(self.__class__.__name__)

    @classmethod
    def make(
        cls,
        id_: str,
        name: str,
        description: str,
        rule: str,
        severity: Severity,
        validated_fields: List[str],
        issue_message: str,
        dependent_fields: List[str],
        for_each: bool = False,
        for_any: bool = False,
    ) -> "CrossFieldValidator":
        validator = cls(
            id_=id_,
            name=name,
            description=description,
            rule=rule,
            severity=severity,
            validated_fields=[EntityCode(field) for field in validated_fields],
            issue_message=CrossFieldIssueMessage(
                message=issue_message,
                dependent_fields=[EntityCode(field) for field in dependent_fields],
            ),
            for_each=for_each,
            for_any=for_any,
        )
        validator._validate()

        return validator

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CrossFieldValidator):
            return False
        return self.id == other.id

    def __repr__(self) -> str:
        return (
            f"CrossFieldValidator(id='{self.id}', name='{self.name}', "
            f"rule='{self.rule}', severity={self.severity}, "
            f"validated_fields={self.validated_fields})"
        )

    def validate(  # noqa: WPS210
        self,
        document: Mapping[EntityCode, Value],
        validators: Mapping[EntityCode, Validator],
    ) -> list[CrossFieldIssues]:
        validated_fields_str = [field.value for field in self.validated_fields]
        validated_fields_set = set(self.validated_fields)
        all_document_fields, validated_fields, rules = [], [], []
        for field_code, field_value in document.items():
            if field_code not in validators:
                continue

            field_validator = validators[field_code]

            data_to_validate = field_validator.preparer(
                field_code,
                field_validator.type_,
                is_required=field_validator.is_required,
            ).prepare(field_value)

            casted_field = self._value_caster.cast_field(data_to_validate)

            all_document_fields.append(casted_field)

            if field_code in validated_fields_set:
                validated_fields.append(casted_field)
                rules.append(self._prepare_rule(field_code.value))

        validation_results = self._business_rules_checker.validate(
            fields=validated_fields,
            rules=rules,
            context_fields=all_document_fields,
        )
        issues: list[FieldValidationIssues] = validation_results.detail

        return [self._build_cross_field_issues(issue, validated_fields_str) for issue in issues]

    def update(
        self,
        name: str,
        description: str,
        rule: str,
        severity: Severity,
        validated_fields: List[EntityCode],
        issue_message: CrossFieldIssueMessage,
        for_each: Optional[bool] = None,
        for_any: Optional[bool] = None,
    ) -> None:
        self.name = name
        self.description = description
        self.rule = rule
        self.severity = severity
        self.validated_fields = validated_fields
        self.issue_message = issue_message

        if for_each is not None:
            self.for_each = for_each

        if for_any is not None:
            self.for_any = for_any

        self._validate()

    def _prepare_rule(self, field_code: str) -> RuleEntity:
        return RuleEntity(
            id=0,
            name=self.name,
            severity=self.severity,
            field_code=field_code,
            document_type_code="type_code",
            rule=self.rule,
            issue_message=self.issue_message.message,
            meta=RuleEntityMeta(
                for_each=self.for_each,
                for_any=self.for_any,
            ),
        )

    def _build_cross_field_issues(
        self,
        issue: FieldValidationIssues,
        validated_fields_str: list[str],
    ) -> CrossFieldIssues:
        field_code = EntityCode(issue.field_code)
        all_messages = issue.errors + issue.warnings

        if all_messages:
            cross_field_issue_list = [
                self._build_cross_field_issue(field_code, validated_fields_str, msg) for msg in all_messages
            ]
        else:
            cross_field_issue_list = [
                CrossFieldIssue(
                    code=field_code,
                    validator_id=self.id,
                    severity=self.severity,
                    validated_fields=validated_fields_str,
                    message=self.issue_message,
                    position=None,
                )
            ]

        return CrossFieldIssues(
            code=field_code,
            errors=cross_field_issue_list if self.severity == Severity.ERROR else [],
            warnings=cross_field_issue_list if self.severity == Severity.WARNING else [],
        )

    def _build_cross_field_issue(
        self,
        field_code: EntityCode,
        validated_fields_str: list[str],
        message: Message,
    ) -> CrossFieldIssue:
        return CrossFieldIssue(
            code=field_code,
            validator_id=self.id,
            severity=self.severity,
            validated_fields=validated_fields_str,
            message=self.issue_message,
            position=self._get_position_from_issue(message),
        )

    def _get_position_from_issue(self, message: Message) -> Optional[Position]:
        has_position_data = any(
            value is not None for value in (message.column, message.row, message.index, message.kv_id)
        )
        if not has_position_data:
            return None

        position = Position()
        if message.column is not None:
            position.column = message.column
        if message.row is not None:
            position.row = message.row
        if message.index is not None:
            position.index = message.index
        if message.kv_id is not None:
            position.kv_id = getattr(message.kv_id, "value", message.kv_id)

        return position

    def _validate(self) -> None:
        try:
            self._rule_validator.validate(
                rule=self.rule,
                validated_fields=[f.value for f in self.validated_fields],
                dependent_fields=[f.value for f in self.issue_message.dependent_fields],
            )
        except SyntaxError:
            message = f"Rule `{self.rule}` for validator `{self.name}` with id `{self.id()}` is not parseable"
            self._logger.warning(message)
            raise UnparseableRuleError(message)
