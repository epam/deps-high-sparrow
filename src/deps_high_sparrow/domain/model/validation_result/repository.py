from typing import Optional, Protocol

from .validation_result import ValidationResult

__all__ = ["IValidationResultRepository"]


class IValidationResultRepository(Protocol):
    def validation_result_of_id(self, entity_id: str, tenant_id: str) -> Optional[ValidationResult]:
        ...

    def delete(self, entity_id: str, tenant_id: str) -> None:
        ...

    def save(self, validation_result: ValidationResult) -> None:
        ...
