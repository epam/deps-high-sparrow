from .base import BusinessException

__all__ = ["ExternalValidatorAlreadyExistsError", "MaxExternalValidatorsExceededError"]


class ExternalValidatorAlreadyExistsError(BusinessException):
    code = "external_validator_already_exists_error"


class MaxExternalValidatorsExceededError(BusinessException):
    code = "max_external_validators_exceeded_error"
