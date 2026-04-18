from typing import Any

from deps_high_sparrow.domain.model import TableDescriptionBuilder

from .base_creator import BaseTableValidatorCreator

__all__ = ["ListTableValidatorCreator"]


class ListTableValidatorCreator(BaseTableValidatorCreator):
    def __init__(self, raw_field: dict[str, Any], builder: TableDescriptionBuilder) -> None:
        super().__init__(raw_field=raw_field, builder=builder)

    def create_columns(self, columns: list[dict[str, Any]]) -> TableDescriptionBuilder:
        self._create_columns(columns)

        return self._builder
