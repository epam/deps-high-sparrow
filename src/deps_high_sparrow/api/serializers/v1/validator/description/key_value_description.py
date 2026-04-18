from typing import Literal

from deps_high_sparrow.domain.model import KeyValueDescription, OperandType

from ....base import ConfiguredBaseModel
from .type_mapping import TYPE_MAPPING, DescriptionGenericType

__all__ = ["SerializedKeyValueDescription"]


class SerializedKeyValueDescription(ConfiguredBaseModel):
    kind: Literal["key_value"] = "key_value"
    key_type: OperandType
    key_meta: DescriptionGenericType
    value_type: OperandType
    value_meta: DescriptionGenericType

    @classmethod
    def from_model(cls, description: KeyValueDescription) -> "SerializedKeyValueDescription":
        key_meta_serializer = TYPE_MAPPING[description.key_meta.__class__]
        value_meta_serializer = TYPE_MAPPING[description.value_meta.__class__]

        return cls(
            key_type=description.key_type,
            key_meta=key_meta_serializer.from_model(description.key_meta),
            value_type=description.value_type,
            value_meta=value_meta_serializer.from_model(description.value_meta),
        )
