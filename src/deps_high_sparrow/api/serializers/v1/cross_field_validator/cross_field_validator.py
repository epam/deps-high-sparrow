from typing import List

from deps_high_sparrow.api.serializers.base import ConfiguredBaseModel
from deps_high_sparrow.domain.model.document_type import CrossFieldValidator
from deps_high_sparrow.domain.model.shared import Severity

__all__ = ["SerializedCrossFieldValidator", "SerializedCrossFieldIssueMessage"]


class SerializedCrossFieldIssueMessage(ConfiguredBaseModel):
    message: str
    dependent_fields: List[str]


class SerializedCrossFieldValidator(ConfiguredBaseModel):
    id: str
    name: str
    description: str
    rule: str
    severity: Severity
    validated_fields: List[str]
    issue_message: SerializedCrossFieldIssueMessage
    for_each: bool
    for_any: bool

    @classmethod
    def from_model(cls, validator: CrossFieldValidator) -> "SerializedCrossFieldValidator":
        return cls(
            id=validator.id(),
            name=validator.name,
            description=validator.description,
            rule=validator.rule,
            severity=validator.severity,
            validated_fields=[field.value for field in validator.validated_fields],
            issue_message=SerializedCrossFieldIssueMessage(
                message=validator.issue_message.message,
                dependent_fields=[field.value for field in validator.issue_message.dependent_fields],
            ),
            for_each=validator.for_each,
            for_any=validator.for_any,
        )
