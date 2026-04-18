from typing import Any

from deps_high_sparrow.domain import DocumentType

from .base_creator import BaseTableValidatorCreator

__all__ = ["TableValidatorCreator"]


class TableValidatorCreator(BaseTableValidatorCreator):
    def __init__(self, raw_field: dict[str, Any], document_type: DocumentType) -> None:
        super().__init__(
            raw_field=raw_field,
            builder=document_type.add_table_validator(raw_field["code"]).with_description(),
        )

    def create(self) -> None:
        if field_constraint := self._raw_field.get("field_data"):
            self._create_columns(field_constraint["columns"])

        if self._is_required:
            self._builder = self._builder.is_required()

        self._builder.build()
