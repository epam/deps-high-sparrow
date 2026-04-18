from typing import Dict, Literal, Type, Union

from deps_high_sparrow.domain.model import (
    GenericDescription,
    KeyValueDescription,
    ListDescription,
    OperandType,
    TableDescription,
)

from ....base import ConfiguredBaseModel
from .key_value_description import SerializedKeyValueDescription
from .table_description import SerializedTableDescription
from .type_mapping import TYPE_MAPPING, DescriptionGenericType

__all__ = ["SerializedListDescription"]


ListDescriptionType = Union[
    GenericDescription,
    KeyValueDescription,
    TableDescription,
]


SerializedListType = Union[
    DescriptionGenericType,
    SerializedKeyValueDescription,
    SerializedTableDescription,
]


DESCRIPTION_TYPE_MAPPING: Dict[Type[ListDescriptionType], Type[SerializedListType]] = {  # noqa: WPS407
    **TYPE_MAPPING,
    KeyValueDescription: SerializedKeyValueDescription,
    TableDescription: SerializedTableDescription,
}


class SerializedListDescription(ConfiguredBaseModel):
    kind: Literal["list"] = "list"
    item_type: OperandType
    meta: SerializedListType

    @classmethod
    def from_model(cls, description: ListDescription) -> "SerializedListDescription":
        meta_serializer = DESCRIPTION_TYPE_MAPPING[description.meta.__class__]

        return cls(
            item_type=description.item_type,
            meta=meta_serializer.from_model(description.meta),
        )
