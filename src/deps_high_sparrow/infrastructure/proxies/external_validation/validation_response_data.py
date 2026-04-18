from typing import Any

from deps_high_sparrow.domain.model import RawIssues

__all__ = ["ExternalValidatorResponse"]


class ExternalValidatorResponse:
    @staticmethod
    def from_raw_response(raw_response: dict[str, Any]) -> list[RawIssues]:
        return [RawIssues(**issues) for issues in raw_response["validationResult"]["issues"]]
