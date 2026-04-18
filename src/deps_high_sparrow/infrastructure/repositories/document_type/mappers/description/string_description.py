from typing import Union

from deps_high_sparrow.domain.model import BasicDescription, StringDescription

from .basic_description import BasicDescriptionMapper

__all__ = ["StringDescriptionMapper"]


class StringDescriptionMapper:
    @staticmethod
    def from_dict(raw_description: dict[str, int]) -> Union[StringDescription, BasicDescription]:
        return StringDescription()

    @staticmethod
    def to_dict(description: Union[StringDescription, BasicDescription]) -> dict[str, int]:
        if isinstance(description, StringDescription):
            return {}
        return BasicDescriptionMapper.to_dict(description)
