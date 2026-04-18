from typing import Optional

from deps_high_sparrow.domain.model import IValidationResultRepository, ValidationResult

__all__ = ["FakeValidationResultRepository"]

ValidationResultIdentifier = tuple[str, str]


class FakeValidationResultRepository(IValidationResultRepository):
    def __init__(self, fake_db: Optional[dict[ValidationResultIdentifier, ValidationResult]] = None) -> None:
        self._validation_result_db: Optional[dict[ValidationResultIdentifier, ValidationResult]] = {}
        if fake_db:
            self._validation_result_db = fake_db

    def __repr__(self) -> str:
        return str(self._validation_result_db)

    def validation_result_of_id(self, entity_id: str, tenant_id: str) -> Optional[ValidationResult]:
        key = self._get_dict_key(entity_id=entity_id, tenant_id=tenant_id)
        return self._validation_result_db.get(key)

    def save(self, validation_result: ValidationResult) -> None:
        key = self._get_dict_key(entity_id=validation_result.id(), tenant_id=validation_result.tenant_id())
        if self._validation_result_db.get(key):
            return

        self._validation_result_db[key] = validation_result

    def update(self, validation_result: ValidationResult) -> None:
        key = self._get_dict_key(entity_id=validation_result.id(), tenant_id=validation_result.tenant_id())
        self._validation_result_db[key] = validation_result

    def delete(self, entity_id: str, tenant_id: str) -> None:
        key = self._get_dict_key(entity_id=entity_id, tenant_id=tenant_id)
        self._validation_result_db.pop(key, None)

    @staticmethod
    def _get_dict_key(*, entity_id: str, tenant_id: str) -> ValidationResultIdentifier:
        return entity_id, tenant_id
