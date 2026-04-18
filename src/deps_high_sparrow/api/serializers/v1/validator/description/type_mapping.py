from typing import Dict, Type, Union

from deps_high_sparrow.domain.model import (
    BasicDescription,
    DateDescription,
    EnumDescription,
    GenericDescription,
    StringDescription,
)

from .basic_description import SerializedBasicDescription
from .date_description import SerializedDateDescription
from .enum_description import SerializedEnumDescription
from .string_description import SerializedStringDescription

__all__ = ["TYPE_MAPPING", "DescriptionGenericType"]


DescriptionGenericType = Union[
    SerializedBasicDescription,
    SerializedStringDescription,
    SerializedEnumDescription,
    SerializedDateDescription,
]


TYPE_MAPPING: Dict[Type[GenericDescription], Type[DescriptionGenericType]] = {  # noqa: WPS407
    StringDescription: SerializedStringDescription,
    BasicDescription: SerializedBasicDescription,
    EnumDescription: SerializedEnumDescription,
    DateDescription: SerializedDateDescription,
}
