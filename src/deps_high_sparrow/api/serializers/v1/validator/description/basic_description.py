from typing import Any, Literal, Optional

from deps_high_sparrow.domain.model import BasicDescription

from ....base import ConfiguredBaseModel

__all__ = ["SerializedBasicDescription"]


class SerializedBasicDescription(ConfiguredBaseModel):
    kind: Literal["basic"] = "basic"
    allowed_values: Optional[list[Any]]
    restricted_values: Optional[list[Any]]

    @classmethod
    def from_model(cls, description: BasicDescription) -> "SerializedBasicDescription":
        return cls(
            allowed_values=description.allowed_values,
            restricted_values=description.restricted_values,
        )
