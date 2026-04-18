from typing import Any

from deps_high_sparrow.domain.model import ExternalValidator

__all__ = ["ExternalValidatorMapper"]


class ExternalValidatorMapper:
    @staticmethod
    def from_dict(raw_external_validator: dict[str, Any]) -> ExternalValidator:
        return ExternalValidator(
            name=raw_external_validator["name"],
            url=raw_external_validator["url"],
        )

    @staticmethod
    def to_dict(external_validator: ExternalValidator) -> dict[str, Any]:
        return {
            "name": external_validator.name,
            "url": external_validator.url,
        }
