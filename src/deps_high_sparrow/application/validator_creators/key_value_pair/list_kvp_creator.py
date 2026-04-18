from typing import Any

from deps_high_sparrow.domain.model import KeyValueDescriptionBuilder

from .base_creator import BaseKVPValidatorCreator

__all__ = ["ListKVPValidatorCreator"]


class ListKVPValidatorCreator(BaseKVPValidatorCreator):
    def __init__(self, raw_field: dict[str, Any], builder: KeyValueDescriptionBuilder) -> None:
        super().__init__(raw_field=raw_field, builder=builder)

    def create_key_value_pair(self, field_constraint: dict[str, Any]) -> KeyValueDescriptionBuilder:
        self._create_key_value_pair(field_constraint)

        return self._builder
