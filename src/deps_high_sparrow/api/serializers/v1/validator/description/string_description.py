from typing import Literal

from deps_high_sparrow.domain.model import StringDescription

from ....base import ConfiguredBaseModel

__all__ = ["SerializedStringDescription"]


class SerializedStringDescription(ConfiguredBaseModel):
    kind: Literal["string"] = "string"

    @classmethod
    def from_model(cls, description: StringDescription) -> "SerializedStringDescription":
        return cls()
