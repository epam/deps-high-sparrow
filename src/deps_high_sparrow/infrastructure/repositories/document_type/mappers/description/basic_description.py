from typing import Any

from deps_high_sparrow.domain.model import BasicDescription

__all__ = ["BasicDescriptionMapper"]


class BasicDescriptionMapper:
    @staticmethod
    def from_dict(raw_description: dict[str, Any]) -> BasicDescription:
        return BasicDescription(
            allowed_values=raw_description["allowed_values"] or [],
            restricted_values=raw_description["restricted_values"] or [],
        )

    @staticmethod
    def to_dict(description: BasicDescription) -> dict[str, Any]:
        return {
            "allowed_values": description.allowed_values if description else None,
            "restricted_values": description.restricted_values if description else None,
        }
