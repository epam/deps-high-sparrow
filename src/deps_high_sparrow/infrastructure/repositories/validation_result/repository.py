from typing import Optional

from sqlalchemy import and_, delete, select
from sqlalchemy.dialects.postgresql import insert

from deps_high_sparrow.domain import IValidationResultRepository, ValidationResult
from deps_high_sparrow.extras import Database

from ...tables import validation_result_table
from .mappers import ValidationResultMapper

__all__ = ["ValidationResultRepository"]


class ValidationResultRepository(IValidationResultRepository):
    def __init__(self, database: Database) -> None:
        self._db = database

    def validation_result_of_id(self, entity_id: str, tenant_id: str) -> Optional[ValidationResult]:
        select_query = select([validation_result_table]).where(
            and_(validation_result_table.c.id == entity_id, validation_result_table.c.tenant_id == tenant_id)
        )

        with self._db.connection() as conn:
            result = conn.execute(select_query).fetchone()

        if result is None:
            return None

        return ValidationResultMapper.from_dict(result)

    def delete(self, entity_id: str, tenant_id: str) -> None:
        delete_query = delete(validation_result_table).where(
            and_(validation_result_table.c.id == entity_id, validation_result_table.c.tenant_id == tenant_id),
        )

        with self._db.connection() as conn:
            conn.execute(delete_query)

    def save(self, validation_result: ValidationResult) -> None:
        raw_validation_result = ValidationResultMapper.to_dict(validation_result)

        insert_query = insert(validation_result_table).values(**raw_validation_result)
        save_query = insert_query.on_conflict_do_update(
            index_elements=[
                validation_result_table.c.id,
                validation_result_table.c.tenant_id,
            ],
            set_={
                "issues": insert_query.excluded.issues,
                "cross_field_issues": insert_query.excluded.cross_field_issues,
            },
        )

        with self._db.connection() as conn:
            conn.execute(save_query)
