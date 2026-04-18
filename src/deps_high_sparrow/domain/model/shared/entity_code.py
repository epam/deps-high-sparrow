from typing import Optional
from uuid import uuid4

from .guards import Guard, ImmutableCheck

__all__ = ["EntityCode"]


class EntityCode:
    value = Guard[str](str, ImmutableCheck())

    def __init__(self, value: Optional[str] = None) -> None:
        self.value = uuid4().hex if value is None else value

    def __call__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"<class '{self.__class__.__name__}': {self.value = }>"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)

    def for_key(self) -> "EntityCode":
        return EntityCode(f"{self.value}__0")

    def for_value(self) -> "EntityCode":
        return EntityCode(f"{self.value}__1")

    def for_array_item(self) -> "EntityCode":
        return EntityCode(f"item_of__{self.value}")
