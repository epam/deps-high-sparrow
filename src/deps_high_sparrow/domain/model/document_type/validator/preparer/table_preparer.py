from typing import Any

from ..validation.dto.prepared_field import (
    Cell,
    Coordinates,
    TableData,
    TableDataToValidate,
)
from .abstract_preparer import AbstractPreparer

__all__ = ["TablePreparer"]


class TablePreparer(AbstractPreparer):
    def prepare(self, value: list[Any]) -> TableDataToValidate:
        data = TableData(
            cells=[
                Cell(
                    value=data,
                    coordinates=Coordinates(column=column, row=row),
                )
                for data, (column, row) in value
            ]
            if value
            else []
        )
        return TableDataToValidate(
            document_id=0,
            field_code=self.code(),
            document_type_code="type_code",
            field_type=self.type.type,
            meta=self.type.description,
            data=data,
            is_required=self.is_required,
        )
