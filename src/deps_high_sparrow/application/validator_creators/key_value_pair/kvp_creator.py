from typing import Any

from deps_high_sparrow.domain import DocumentType

from .base_creator import BaseKVPValidatorCreator

__all__ = ["KVPValidatorCreator"]


class KVPValidatorCreator(BaseKVPValidatorCreator):
    def __init__(self, raw_field: dict[str, Any], document_type: DocumentType) -> None:
        super().__init__(
            raw_field=raw_field,
            builder=document_type.add_key_value_validator(raw_field["code"]).with_description(),
        )

    def create(self) -> None:
        self._create_key_value_pair(self._raw_field["field_data"])

        self._builder.build()

    def _create_key_value_pair(self, field_constraint: dict[str, Any]) -> None:
        super()._create_key_value_pair(field_constraint)

        if self._raw_field["required"]:
            self._builder = self._builder.is_required()
