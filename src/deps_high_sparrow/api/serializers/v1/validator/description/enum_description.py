from typing import Literal

from deps_high_sparrow.domain.model import EnumDescription

from ....base import ConfiguredBaseModel

__all__ = ["SerializedEnumDescription"]


class SerializedEnumDescription(ConfiguredBaseModel):
    kind: Literal["enum"] = "enum"
    options: list[str]

    @classmethod
    def from_model(cls, description: EnumDescription) -> "SerializedEnumDescription":
        return cls(
            options=description.options,
        )
