from typing import Literal

from deps_high_sparrow.domain.model import (
    ColumnDescription,
    OperandType,
    TableDescription,
)

from ....base import ConfiguredBaseModel
from .type_mapping import TYPE_MAPPING, DescriptionGenericType

__all__ = ["SerializedTableDescription"]


class SerializedColumnDescription(ConfiguredBaseModel):
    index: int
    is_required: bool
    item_type: OperandType
    meta: DescriptionGenericType

    @classmethod
    def from_model(cls, description: ColumnDescription) -> "SerializedColumnDescription":
        meta_serializer = TYPE_MAPPING[description.meta.__class__]

        return cls(
            index=description.index,
            is_required=description.is_required,
            item_type=description.item_type,
            meta=meta_serializer.from_model(description.meta),
        )


class SerializedTableDescription(ConfiguredBaseModel):
    kind: Literal["table"] = "table"
    columns: list[SerializedColumnDescription]

    @classmethod
    def from_model(cls, description: TableDescription) -> "SerializedTableDescription":
        return cls(columns=[SerializedColumnDescription.from_model(column) for column in description.columns])
