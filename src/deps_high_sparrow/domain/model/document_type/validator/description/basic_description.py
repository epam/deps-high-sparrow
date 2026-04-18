from typing import Any, Optional

from ....shared import Guard, ImmutableCheck
from .generic_description import GenericDescription

__all__ = ["BasicDescription"]


class BasicDescription(GenericDescription):
    allowed_values = Guard[list[Any]](list, ImmutableCheck())
    restricted_values = Guard[list[Any]](list, ImmutableCheck())

    def __init__(
        self,
        allowed_values: Optional[list[Any]] = None,
        restricted_values: Optional[list[Any]] = None,
    ) -> None:
        self.allowed_values = allowed_values or []
        self.restricted_values = restricted_values or []

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, self.__class__)
            and self.allowed_values == other.allowed_values
            and self.restricted_values == other.restricted_values
        )
