from pydantic import Field

from deps_high_sparrow.domain.model import ValidationResult

from ...base import ConfiguredBaseModel
from .issues import SerializedIssues

__all__ = ["SerializedValidationResult"]


class SerializedValidationResult(ConfiguredBaseModel):
    is_valid: bool = Field(..., alias="isValid")
    detail: list[SerializedIssues]

    @classmethod
    def from_model(cls, validation_result: ValidationResult) -> "SerializedValidationResult":
        return cls(
            is_valid=validation_result.is_valid,
            detail=[
                SerializedIssues.from_model(
                    entity_id=validation_result.id.value,
                    issues=issues,
                    cross_field_issues=validation_result.cross_field_issues,
                )
                for issues in validation_result.issues.values()
            ],
        )
