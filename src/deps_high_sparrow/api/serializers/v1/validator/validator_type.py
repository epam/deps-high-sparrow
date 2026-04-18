from typing import Dict, Optional, Type, Union

from pydantic import Field

from deps_high_sparrow.domain.model import (
    GenericDescription,
    KeyValueDescription,
    ListDescription,
    OperandType,
    TableDescription,
    ValidatorType,
)

from ...base import ConfiguredBaseModel
from .description import *

__all__ = ["SerializedValidatorType"]

DescriptionType = Union[
    GenericDescription,
    KeyValueDescription,
    TableDescription,
    ListDescription,
]


SerializedDescriptionType = Union[
    SerializedStringDescription,
    SerializedEnumDescription,
    SerializedDateDescription,
    SerializedKeyValueDescription,
    SerializedListDescription,
    SerializedTableDescription,
    SerializedBasicDescription,
]


VALIDATOR_TYPE_DESCRIPTION_MAP: Dict[Type[DescriptionType], Type[SerializedDescriptionType]] = {  # noqa: WPS407
    **TYPE_MAPPING,
    KeyValueDescription: SerializedKeyValueDescription,
    TableDescription: SerializedTableDescription,
    ListDescription: SerializedListDescription,
}


class SerializedValidatorType(ConfiguredBaseModel):
    type: OperandType
    description: Optional[SerializedDescriptionType] = Field(default=None, discriminator="kind")

    @classmethod
    def from_model(cls, validator_type: ValidatorType) -> "SerializedValidatorType":
        if validator_type.description is None:
            return cls(type=validator_type.type)

        description_serializer = VALIDATOR_TYPE_DESCRIPTION_MAP[validator_type.description.__class__]

        return cls(
            type=validator_type.type,
            description=description_serializer.from_model(validator_type.description),
        )
