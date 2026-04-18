from ....shared import Guard, ImmutableCheck
from .generic_description import GenericDescription

__all__ = ["EnumDescription"]


class EnumDescription(GenericDescription):
    options = Guard[list[str]](list, ImmutableCheck())

    def __init__(self, options: list[str]) -> None:
        self.options = options

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.options == other.options
