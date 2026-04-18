from typing import Any, Union

from deps_high_sparrow.domain.model import BasicDescription, EnumDescription

from .basic_description import BasicDescriptionMapper

__all__ = ["EnumDescriptionMapper"]


class EnumDescriptionMapper:
    @staticmethod
    def from_dict(raw_description: dict[str, Any]) -> Union[EnumDescription, BasicDescription]:
        options = raw_description.get("options")

        if options is None:
            return BasicDescription()

        return EnumDescription(options=options)

    @staticmethod
    def to_dict(description: Union[EnumDescription, BasicDescription]) -> dict[str, Any]:
        if isinstance(description, EnumDescription):
            return {
                "options": description.options if description else None,
            }
        return BasicDescriptionMapper.to_dict(description)
