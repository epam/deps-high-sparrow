from .base import HighSparrowException, NotFoundError

__all__ = ["DocumentTypeNotFound", "ValidatorNotFound", "RuleAlreadyExistsError"]


class DocumentTypeNotFound(NotFoundError):
    code = "document_type_not_found"

    def __init__(self, id_: str) -> None:
        super().__init__(f"Document type with id: `{id_}` not found")


class ValidatorNotFound(NotFoundError):
    code = "validator_not_found"

    def __init__(self, code: str) -> None:
        super().__init__(f"Validator with code: `{code}` not found")


class RuleAlreadyExistsError(HighSparrowException):
    code = "rule_already_exists_error"

    def __init__(self, name: str) -> None:
        super().__init__(f"Rule with name: `{name}` already exists in validator")
