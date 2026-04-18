from typing import Any

from deps_high_sparrow.domain.model import EntityCode
from deps_high_sparrow.domain.model.validation_result import CrossFieldIssueMessage

__all__ = ["CrossFieldIssueMessageMapper"]


class CrossFieldIssueMessageMapper:
    @staticmethod
    def from_dict(raw_message: dict[str, Any]) -> CrossFieldIssueMessage:
        return CrossFieldIssueMessage(
            message=raw_message["message"],
            dependent_fields=[EntityCode(field) for field in raw_message["dependent_fields"]],
        )

    @staticmethod
    def to_dict(message: CrossFieldIssueMessage) -> dict[str, Any]:
        return {
            "message": message.message,
            "dependent_fields": [field.value for field in message.dependent_fields],
        }
