from typing import Union

from deps_high_sparrow.domain.model import BasicDescription, DateDescription

from .basic_description import BasicDescriptionMapper

__all__ = ["DateDescriptionMapper"]


class DateDescriptionMapper:
    @staticmethod
    def from_dict(raw_description: dict[str, str]) -> Union[DateDescription, BasicDescription]:
        format_ = raw_description.get("format")

        if format_ is None:
            return BasicDescription()

        return DateDescription(format=format_)

    @staticmethod
    def to_dict(description: Union[DateDescription, BasicDescription]) -> dict[str, str]:
        if isinstance(description, DateDescription):
            return {
                "format": description.format if description else None,
            }
        return BasicDescriptionMapper.to_dict(description)
