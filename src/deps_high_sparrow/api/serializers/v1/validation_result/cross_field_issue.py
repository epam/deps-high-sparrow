import logging
from typing import Optional

from pydantic import Field

from deps_high_sparrow.domain.model import CrossFieldIssue, Severity

from ...base import ConfiguredBaseModel

__all__ = ["SerializedCrossFieldIssue"]

logger = logging.getLogger(__name__)


class SerializedCrossFieldIssue(ConfiguredBaseModel):
    code: str
    validator_id: str = Field(..., alias="validatorId")
    severity: Severity
    validated_fields: list[str] = Field(..., alias="validatedFields")
    message: str

    column: Optional[int]
    row: Optional[int]
    index: Optional[int]
    kv_id: Optional[str] = Field(alias="kvId")

    @classmethod
    def from_model(cls, cross_field_issue: CrossFieldIssue) -> "SerializedCrossFieldIssue":
        return cls(
            code=cross_field_issue.code.value,
            validator_id=cross_field_issue.validator_id.value,
            severity=cross_field_issue.severity,
            validated_fields=cross_field_issue.validated_fields,
            message=cross_field_issue.message.message,
            column=cross_field_issue.position.column if cross_field_issue.position else None,
            row=cross_field_issue.position.row if cross_field_issue.position else None,
            index=cross_field_issue.position.index if cross_field_issue.position else None,
            kv_id=cross_field_issue.position.kv_id if cross_field_issue.position else None,
        )
