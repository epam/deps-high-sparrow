from typing import List

from .base import BusinessException, NotFoundError

__all__ = [
    "CrossFieldValidatorNotFound",
    "MaxCrossFieldValidatorsExceededError",
    "InvalidFieldCodesError",
    "CrossFieldValidatorAlreadyExistsError",
    "WrongCrossFieldValidatorMessageError",
    "RuleFieldReferencesMismatchError",
    "UnparseableRuleError",
]


class CrossFieldValidatorNotFound(NotFoundError):
    code = "cross_field_validator_not_found"

    def __init__(self, id_: str) -> None:
        super().__init__(f"Cross-field validator with id: `{id_}` not found")


class MaxCrossFieldValidatorsExceededError(BusinessException):
    code = "max_cross_field_validators_exceeded_error"


class InvalidFieldCodesError(BusinessException):
    code = "invalid_field_codes"

    def __init__(self, field_codes: List[str]) -> None:
        super().__init__(f"Invalid field codes: {', '.join(field_codes)}")


class CrossFieldValidatorAlreadyExistsError(BusinessException):
    code = "cross_field_validator_already_exists_error"


class WrongCrossFieldValidatorMessageError(BusinessException):
    code = "cross_field_validator_wrong_message_format"


class RuleFieldReferencesMismatchError(BusinessException):
    code = "rule_field_references_mismatch"

    def __init__(self, unreferenced_fields: list[str], unknown_fields: list[str]) -> None:
        super().__init__(f"Unreferenced fields: {unreferenced_fields}. Unknown fields in rule: {unknown_fields}")


class UnparseableRuleError(BusinessException):
    code = "unparseable_rule"
