from ....shared import Guard, ImmutableCheck
from .generic_description import GenericDescription

__all__ = ["DateDescription"]


class DateDescription(GenericDescription):
    format = Guard[str](str, ImmutableCheck())

    def __init__(self, format: str) -> None:
        self.format = format

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.format == other.format
