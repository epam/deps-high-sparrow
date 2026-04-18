from typing import Literal

from deps_high_sparrow.domain.model import DateDescription

from ....base import ConfiguredBaseModel

__all__ = ["SerializedDateDescription"]


class SerializedDateDescription(ConfiguredBaseModel):
    kind: Literal["date"] = "date"
    format: str

    @classmethod
    def from_model(cls, description: DateDescription) -> "SerializedDateDescription":
        return cls(
            format=description.format,
        )
